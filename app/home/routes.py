from flask import Blueprint, jsonify
from app.models import db


home_bp = Blueprint("home_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static")


@home_bp.route("/")
def hello_world():
    return jsonify(hello="world")

