from flask import Blueprint, render_template, url_for
from app.models import db


home_bp = Blueprint("home_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static")


@home_bp.route("/")
def index():
    return render_template("index.html")

@home_bp.route("/profile")
def profile():
    return render_template("profile.html")