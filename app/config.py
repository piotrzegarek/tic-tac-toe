"""Flask App configuration."""
from os import environ


class Config:
    """Base config."""
    SECRET_KEY = environ.get('SECRET_KEY')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'


class ProdConfig(Config):
    """Production config."""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DATABASE_URI = environ.get('DEV_DATABASE_URI')