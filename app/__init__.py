import os

from flask import Flask
from flask_login import LoginManager

from app.models import db, User
from app.game.events import sio

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Load config
    if os.getenv("FLASK_CONFIG") == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    # Initialize plugins
    db.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.init_app(app)
    sio.init_app(app)

    with app.app_context():
        # Register blueprints
        from .home.routes import home_bp
        from .profile.routes import profile_bp
        from .auth.routes import auth_bp
        from .game.routes import game_bp
        app.register_blueprint(home_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(game_bp, url_prefix="/play")
        app.register_blueprint(profile_bp, url_prefix="/profile")

        # User loader
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app