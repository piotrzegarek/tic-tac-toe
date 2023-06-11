from flask_login import current_user

from app.models import GameSession, Game
from app.enums import GameResult


def get_games_data(history_date: str) -> dict:
    game_sessions = GameSession.query.filter_by(user_id=current_user.id, date=history_date).all()
    result = {}
    for session in game_sessions:
        games_data = []
        wins_count = 0
        losses_count = 0
        draws_count = 0
        games = Game.query.filter_by(game_session_id=session.id).all()
        for game in games:
            print(game.game_result)
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

        result[session.id] = {'wins': wins_count, 
                              'losses': losses_count, 
                              'draws': draws_count, 
                              'games_count': len(games),
                              'games': games_data}
        
    return result

