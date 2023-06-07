
from os import environ, path
from dotenv import load_dotenv

from flask import Flask
from app.config import ProdConfig, DevConfig

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


def create_app():
    app = Flask(__name__)

    flask_config = environ.get("FLASK_CONFIG")
    if flask_config == "production":
        app.config.from_object(ProdConfig)
    else:
        app.config.from_object(DevConfig)

    return app