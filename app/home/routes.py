from flask import Blueprint, jsonify
from app.models import db


home_bp = Blueprint("home_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static")


@home_bp.route("/")
def index():
    return jsonify(hello="index")

@home_bp.route("/profile")
def profile():
    return jsonify(hello="profile")