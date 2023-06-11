from datetime import datetime

from .socket_manager import sio
from flask_login import current_user
from flask import request

from app.models import db, GameSession, Game
from app.game.games_server import server


@sio.on('connect')
def handle_connect():
    sid = request.sid
    print('connect ', sid, ' User: ', current_user.username)
    print("Creating game session")
    new_session = GameSession(
        user_id = current_user.id,
        socket_id = sid,
        date = datetime.now().strftime("%m/%d/%Y")
    )
    db.session.add(new_session)
    db.session.commit()
    db.session.flush()
    # TODO: Add error handling
    sio.emit('connect-response', {'success': True, 'game_session_id': new_session.id})


@sio.on('addTickets')
def handle_addTickets(data):
    """ Check if user has 0 tickets and add 10 tickets to the session."""
    game_session_id = data.get('game_session_id')
    game_session = GameSession.query.filter_by(id=game_session_id).first()
    if game_session.tickets == 0:
        game_session.tickets = 10
        db.session.commit()
        sio.emit('addTickets-response', {'success': True})
    else:
        error_msg = 'Cannot add tickets to session.'
        sio.emit('addTickets-response', {'success': False, 'error': error_msg})


@sio.on('startGame')
def handle_startGame(data):
    game_session_id = data.get('game_session_id')
    game_session = GameSession.query.filter_by(id=game_session_id).first()
    if game_session.tickets >= 3:
        game_session.tickets -= 3
        new_game = server.createGame(game_session_id, 'singleplayer')
        game_id = new_game.game.id
        player = new_game.player1
        db.session.commit()

        sio.emit('startGame-response', {'success': True, 'tickets': game_session.tickets, 'game_id': game_id, 
                                        'player': player, 'turn': new_game.turn, 'board': new_game.board})
    elif game_session.tickets == 0:
        error_msg = 'Not enough tickets to start game'
        sio.emit('startGame-response', {'success': False, 'error': error_msg})
    else:
        sio.emit('endSession')


@sio.on('makeMove')
def handle_move(data):
    game_id = data.get('game_id')
    player = data.get('player')
    game = server.getGame(game_id)
    result = game.makeMove(data.get('square_id'), player)
    if result:
        sio.emit('makeMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id'), 'board': game.board})
        is_winner = game.checkWinner()
        if is_winner:
            game_session_id = game.game.game_session_id
            game_session = GameSession.query.filter_by(id=game_session_id).first()
            if is_winner == game.player1:
                game_session.tickets += 4
                db.session.commit()
            game.endGame()

            server.deleteGame(game_id)
            sio.emit('gameOver', {'winner': is_winner, 'tickets': game_session.tickets})
    else:
        sio.emit('makeMove-response', {'success': False, 'error': 'Invalid move'})
    
    
@sio.on('waitForMove')
def handle_waitForMove(data):
    game_id = data.get('game_id')
    game = server.getGame(game_id)
    if game is None:
        return
    if game.mode == 'singleplayer':
        waitForComputer(game, data)


def waitForComputer(game, data):
    if game.checkWinner() is None:
        game.makeMove(game.player2.generateMove(game.board), game.player2.player)
        sio.emit('enemyMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id'), 'board': game.board})
        is_winner = game.checkWinner()
        if is_winner:
            game.endGame()
            game_session_id = game.game.game_session_id
            game_session = GameSession.query.filter_by(id=game_session_id).first()
            server.deleteGame(game.game.id)
            sio.emit('gameOver', {'winner': is_winner, 'tickets': game_session.tickets})


@sio.on('exitGame')
def handle_exitGame(data):
    game_id = data.get('game_id')
    game = server.getGame(game_id)
    game.endGame()
    server.deleteGame(game_id)
    sio.emit('exitGame-response', {'success': True})


@sio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    game_session = GameSession.query.filter_by(socket_id=sid).first()
    if game_session:
        games = Game.query.filter_by(game_session_id=game_session.id).all()
        for game in games:
            if game.id in server.games:
                game_object = server.getGame(game.id)
                game_object.endGame()
                server.deleteGame(game.id)
