from flask_login import current_user

from app.models import GameSession, Game


def get_games_data(history_date: str) -> dict:
    """ Get dict with games data played in sessions within selected date."""
    game_sessions = GameSession.query.filter_by(user_id=current_user.id, date=history_date).all()
    result = {}
    for session in game_sessions:
        result[session.id] = get_session_games(session.id)
        
    return result


def get_session_games(session_id: int) -> dict:
    """ Get dict with games data played in session."""
    games_data = []
    wins_count, losses_count, draws_count = 0, 0, 0
    games = Game.query.filter_by(game_session_id=session_id).all()
    for game in games:
        if game.game_result == 'win':
            wins_count += 1
        elif game.game_result == 'draw':
            draws_count += 1
        else:
            losses_count += 1
        
        games_data.append({
            'game_result': game.game_result.value,
            'game_time': game.game_time
        })

    return {'wins': wins_count,
            'losses': losses_count,
            'draws': draws_count,
            'games_count': len(games),
            'games': games_data}