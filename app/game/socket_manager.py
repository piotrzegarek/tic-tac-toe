from datetime import datetime

from flask_login import current_user
from flask import request
from flask_socketio import SocketIO, join_room, leave_room, emit, send

from app.models import db, GameSession, Game
from app.game.games_server import server


sio = SocketIO()


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
    sio.emit('connect-response', {'success': True, 'game_session_id': new_session.id}, to=request.sid)


@sio.on('addTickets')
def handle_addTickets(data):
    """ Check if user has 0 tickets and add 10 tickets to the session."""
    game_session_id = data.get('game_session_id')
    game_session = GameSession.query.filter_by(id=game_session_id).first()
    if game_session.tickets == 0:
        game_session.tickets = 10
        db.session.commit()
        sio.emit('addTickets-response', {'success': True}, to=request.sid)
    else:
        error_msg = 'Cannot add tickets to session.'
        sio.emit('addTickets-response', {'success': False, 'error': error_msg}, to=request.sid)


@sio.on('startGame')
def handle_startGame(data):
    game_session_id = data.get('game_session_id')
    game_session = GameSession.query.filter_by(id=game_session_id).first()
    if game_session.tickets >= 3:
        game_session.tickets -= 3
        new_game, player = server.createGame(game_session_id, 'singleplayer')
        game_id = new_game.games[0].id
        db.session.commit()

        sio.emit('startGame-response', {'success': True, 'tickets': game_session.tickets, 'game_id': game_id, 
                                        'player': player, 'turn': new_game.turn, 'board': new_game.board}, to=request.sid)
    elif game_session.tickets == 0:
        error_msg = 'Not enough tickets to start game'
        sio.emit('startGame-response', {'success': False, 'error': error_msg}, to=request.sid)
    else:
        sio.emit('endSession', to=request.sid)


@sio.on('startGame-multiplayer')
def handle_startGame_multiplayer(data):
    game_session_id = data.get('game_session_id')
    game_session = GameSession.query.filter_by(id=game_session_id).first()
    if game_session.tickets >= 3:
        game_session.tickets -= 3
        new_game, player = server.createGame(game_session_id, 'multiplayer')
        print("Created new multiplayer game")
        print(new_game.player1, new_game.player2)
        game_id = new_game.games[0].id
        db.session.commit()
        print(f"Player {player} joined game {game_id}")
        join_room(f"{game_id}", request.sid)
        sio.emit('startGame-response', {'success': True, 'tickets': game_session.tickets, 'game_id': game_id,
                                        'player': player, 'turn': new_game.turn, 'board': new_game.board, 'oponent': new_game.player2},
                                        to=f"{game_id}")
    elif game_session.tickets == 0:
        error_msg = 'Not enough tickets to start game'
        sio.emit('startGame-response', {'success': False, 'error': error_msg}, to=request.sid)
    else:
        sio.emit('endSession', to=request.sid)


@sio.on('makeMove')
def handle_move(data):
    game_id = data.get('game_id')
    player = data.get('player')
    game = server.getGame(game_id)
    result = game.makeMove(data.get('square_id'), player)
    if result:
        sio.emit('makeMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id'), 'board': game.board}, to=request.sid)
        is_winner = game.checkWinner()
        if is_winner:
            game_session_id = game.games[0].game_session_id
            game_session = GameSession.query.filter_by(id=game_session_id).first()
            if is_winner == game.player1:
                game_session.tickets += 4
                db.session.commit()
            game.endGame()

            server.deleteGame(game_id)
            sio.emit('gameOver', {'winner': is_winner, 'tickets': game_session.tickets}, to=request.sid)
    else:
        sio.emit('makeMove-response', {'success': False, 'error': 'Invalid move'}, to=request.sid)
    

@sio.on('makeMove-multiplayer')
def handle_move_multiplayer(data):
    game_id = data.get('game_id')
    player = data.get('player')
    game = server.getGame(game_id)
    result = game.makeMove(data.get('square_id'), player)
    if result:
        sio.emit('makeMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id'), 'board': game.board}, to=f"{game_id}")
        is_winner = game.checkWinner()
        if is_winner:
            if is_winner == game.player1:
                game_session_id = game.games[0].game_session_id
                game_session = GameSession.query.filter_by(id=game_session_id).first()
                game_session.tickets += 4
                winner_tickets = game_session.tickets
            elif is_winner == game.player2 and game.mode == 'multiplayer':
                game_session_id = game.games[1].game_session_id
                game_session = GameSession.query.filter_by(id=game_session_id).first()
                game_session.tickets += 4
                winner_tickets = game_session.tickets
            else:
                winner_tickets = 0
            db.session.commit()

            game.endGame()
            server.deleteGame(game_id)
            sio.emit('gameOver', {'winner': is_winner, 'tickets': winner_tickets}, to=f"{game_id}")

    else:
        sio.emit('makeMove-response', {'success': False, 'error': 'Invalid move'}, to=request.sid)

    
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
        sio.emit('enemyMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id'), 'board': game.board}, to=request.sid)
        is_winner = game.checkWinner()
        if is_winner:
            game.endGame()
            game_session_id = game.games[0].game_session_id
            game_session = GameSession.query.filter_by(id=game_session_id).first()
            server.deleteGame(game.games[0].id)
            sio.emit('gameOver', {'winner': is_winner, 'tickets': game_session.tickets}, to=request.sid)


@sio.on('exitGame')
def handle_exitGame(data):
    game_id = data.get('game_id')
    game = server.getGame(game_id)
    gamemode = game.mode
    game.endGame()
    server.deleteGame(game_id)
    if gamemode == 'multiplayer':
        leave_room(f"{game_id}", request.sid)
        sio.emit('exitGame-response', {'success': True}, to=f"{game_id}")


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
