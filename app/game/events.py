from .socket_manager import socketio
from flask_login import current_user

@socketio.on('connect')
def handle_connect():
    print('Client connected: ', current_user.username)
    print("Creating game session")


@socketio.on('disconnect')
def handle_disconnect():
    print("Ending game session for: ", current_user.username)
    print('Client disconnected')


@socketio.on('addTickets')
def handle_addTickets():
    # check if can add tickets to game and return true or false
    response = False
    error_msg = 'Cannot add tickets to session.'

    socketio.emit('addTickets-response', {'success': response, 'error': error_msg})
    print('Adding tickets')


@socketio.on('startGame')
def handle_startGame():
    # check if can start game and return success and error message
    response = True
    error_msg = 'Not enough tickets to start game'

    socketio.emit('startGame-response', {'success': response, 'error': error_msg, 'tickets': 7})
    print('Starting game')