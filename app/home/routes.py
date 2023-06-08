from flask import Blueprint, render_template, url_for
from flask_login import login_required
from app.models import db


home_bp = Blueprint("home_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static")


@home_bp.route("/")
@login_required
def home():
    return render_template("home.html")