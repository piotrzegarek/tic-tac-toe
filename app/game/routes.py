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

