import random
from .socket_manager import sio
from flask_login import current_user
from flask import request

from app.models import db, GameSession
from app.game.game_engine import GameEngine


class Server():
    def __init__(self):
        self.games = {}

    def createGame(self, game_session_id):
        new_game = GameEngine(game_session_id)
        self.games[new_game.game.id] = new_game

        return new_game.game.id

    def getGame(self, game_id):
        return self.games[game_id]

    def deleteGame(self, game_id):
        del self.games[game_id]

server = Server()


@sio.on('connect')
def handle_connect():
    sid = request.sid
    print('connect ', sid, ' User: ', current_user.username)
    print("Creating game session")
    new_session = GameSession(
        user_id = current_user.id,
        socket_id = sid
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
    if game_session.tickets > 3:
        game_session.tickets -= 3
        game_id = server.createGame(game_session_id)
        player = random.choice(['x', 'o'])
        sio.emit('startGame-response', {'success': True, 'tickets': game_session.tickets, 'game_id': game_id, 'player': player})
    else:
        error_msg = 'Not enough tickets to start game'
        sio.emit('startGame-response', {'success': False, 'error': error_msg})


@sio.on('makeMove')
def handle_move(data):
    game_id = data.get('game_id')
    player = data.get('player')
    game = server.getGame(game_id)
    result = game.makeMove(data.get('square_id'), player)
    if result:
        sio.emit('makeMove-response', {'success': True, 'turn': game.turn, 'square_id': data.get('square_id')})
        is_winner = game.checkWinner()
        if is_winner:
            server.deleteGame(game_id)
            sio.emit('gameOver', {'winner': is_winner})
    else:
        sio.emit('makeMove-response', {'success': False, 'error': 'Invalid move'})
    
