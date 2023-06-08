import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")

class ProductionConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
