from flask import Blueprint, render_template
from flask_login import login_required

profile_bp = Blueprint("profile_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

@profile_bp.route("/")
@login_required
def profile():
    # Create game sess
    return render_template("profile.html")