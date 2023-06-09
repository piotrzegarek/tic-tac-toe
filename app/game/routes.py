from flask import Blueprint, render_template
from flask_login import login_required

game_bp = Blueprint("game_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

from app.models import db, GameSession, Game
from app.game.game_engine import GameEngine


@game_bp.route("/")
@login_required
def game_session():
    return render_template("game.html")

@game_bp.route("create-game", methods=["POST"])
@login_required
def create_game():
    # Create game in session
    # data = requests.get_json()
    # game_session_id = data["game_session_id"]
    # game = GameEngine(game_session_id)

    return "Create game"
