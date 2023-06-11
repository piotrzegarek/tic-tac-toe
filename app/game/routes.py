from flask import Blueprint, render_template
from flask_login import login_required

game_bp = Blueprint("game_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

@game_bp.route("/")
@login_required
def game_session():
    """ Render game page for singleplayer. """
    return render_template("game.html", game_type="singleplayer")

@game_bp.route("/multiplayer")
@login_required
def game_session_multi():
    """ Render game page for multiplayer. """
    return render_template("game.html", game_type="multiplayer")

