from datetime import datetime
from flask import request
from flask_login import current_user

from app.models import db, Game, GameSession
from .socket_manager import sio


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


@sio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print('disconnect ', sid, ' User: ', current_user.username)


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
        GameEngine(game_session_id)
        db.session.commit()
        sio.emit('startGame-response', {'success': True, 'tickets': game_session.tickets})
    else:
        error_msg = 'Not enough tickets to start game'
        sio.emit('startGame-response', {'success': False, 'error': error_msg})


class GameEngine():
    def __init__(self, session_id: int):
        self.game = self.initGame(session_id)
        self.board = [[0 for _ in range(3)] for _ in range(3)]
        self.turn = 'x'

    def initGame(self, session_id: int):
        new_game = Game(
            game_session_id=session_id,
            date = datetime.now().strftime("%Y/%m/%d")
        )
        db.session.add(new_game)
        db.session.commit()
        db.session.flush()

        return new_game
    
    # @socketio.on('connect')
    # def handle_move(self, data):
    #     print('received move: ' + str(data))
    #     self.board[data['row']][data['col']] = data['player']
    #     self.turn = 'o' if self.turn == 'x' else 'x'
    #     socketio.emit('move', data, broadcast=True)