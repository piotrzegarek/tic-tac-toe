from flask import Blueprint, render_template
from flask_login import login_required

profile_bp = Blueprint("profile_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

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
        games = Game.query.filter_by(game_session_id=session.id).all()
        for game in games:
            games_data.append({
                'game_result': game.game_result.value,
                'game_time': game.game_time
            })
        result[session.id] = games_data
    return jsonify(result)