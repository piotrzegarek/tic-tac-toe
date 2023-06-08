import requests
from datetime import datetime
from flask import Blueprint

game_bp = Blueprint("game_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

from app.models import db, GameSession, Game
from app.game.game_engine import GameEngine


@game_bp.route("/")
def game_session():
    # Create game sess
    return "Game session"

@game_bp.route("create-game", methods=["POST"])
def create_game():
    # Create game in session
    # data = requests.get_json()
    # game_session_id = data["game_session_id"]
    # game = GameEngine(game_session_id)

    return "Create game"
