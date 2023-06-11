from datetime import datetime
from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required

profile_bp = Blueprint("profile_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

from app.profile.functions import get_games_data

@profile_bp.route("/")
@login_required
def profile():
    date = datetime.now().strftime("%m/%d/%Y")
    return render_template("profile.html", date=date)


@profile_bp.route("/get_games.json", methods=["POST"])
@login_required
def get_games():
    data = request.get_json()
    try:
        history_date = data.get('date')
        result = get_games_data(history_date)
        
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return jsonify({'error': 'Something went wrong'}), 500