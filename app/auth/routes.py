from flask import Blueprint, jsonify
from app.models import db


auth_bp = Blueprint("auth_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static")

@auth_bp.route("/login")
def login_user():
    return jsonify(hello="login")

@auth_bp.route("/logout")
def logout_user():
    return jsonify(hello="logout")

@auth_bp.route("/signup")
def signup_user():
    return jsonify(hello="signup")