import os

from flask import Flask
from flask_login import LoginManager, login_user
from app.models import db

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
    login_manager.init_app(app)

    with app.app_context():
        # Register blueprints
        from .home.routes import home_bp
        app.register_blueprint(home_bp)
        from .auth.routes import auth_bp
        app.register_blueprint(auth_bp)

    return app