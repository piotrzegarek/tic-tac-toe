import os

from flask import Flask
from app.models import db


def create_app():
    app = Flask(__name__)

    # Load config
    if os.getenv("FLASK_CONFIG") == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    # Initialize plugins
    db.init_app(app)

    with app.app_context():
        # Register blueprints
        from .home.routes import home_bp
        app.register_blueprint(home_bp, url_prefix="/")

    return app