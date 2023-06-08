from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User


auth_bp = Blueprint("auth_bp", __name__, 
                    template_folder="templates", 
                    static_folder="static",
                    static_url_path="/auth/static")


@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get('remember') else False

    if username == "" or password == "":
        flash("Please fill out all fields.")
        return redirect(url_for("auth_bp.login"))

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("auth_bp.login"))
    
    login_user(user, remember=remember)

    return redirect(url_for("home_bp.home"))


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/signup")
def signup():
    return render_template("signup.html")


@auth_bp.route("/signup", methods=["POST"])
def signup_post():
    username = request.form.get("username")
    password = request.form.get("password")
    repeat_password = request.form.get("passwordRepeat")

    if username == "" or password == "" or repeat_password == "":
        flash("Please fill out all fields.")
        return redirect(url_for("auth_bp.signup"))
    
    if password != repeat_password:
        flash("Passwords do not match.")
        return redirect(url_for("auth_bp.signup"))

    user = User.query.filter_by(username=username).first()
    if user:
        flash('Username already exists. Try logging in.')
        return redirect(url_for("auth_bp.signup"))
    
    new_user = User(username=username, password=generate_password_hash(password, method="sha256"))
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth_bp.login"))