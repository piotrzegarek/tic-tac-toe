from flask import Blueprint, render_template, url_for
from flask_login import login_required
from app.models import db


home_bp = Blueprint("home_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static",
                    static_url_path="/home/static")


@home_bp.route("/")
@login_required
def home():
    """ Render home page. """
    return render_template("home.html")