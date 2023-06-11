from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

profile_bp = Blueprint("profile_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

from app.models import GameSession, Game
from app.enums import GameResult


@profile_bp.route("/")
@login_required
def profile():
    return render_template("profile.html")


@profile_bp.route("/get_games.json", methods=["POST", "GET"])
@login_required
def get_games():
    # data = request.get_json()
    # history_date = data.get("history_date")
    game_sessions = GameSession.query.filter_by(user_id=current_user.id).all()
    result = {}
    for session in game_sessions:
        games_data = []
        wins_count = 0
        losses_count = 0
        draws_count = 0
        games = Game.query.filter_by(game_session_id=session.id).all()
        for game in games:
            print(game.game_result)
            if game.game_result == GameResult.WIN:
                wins_count += 1
            elif game.game_result == GameResult.DRAW:
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
    return jsonify(result)