from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from app.enums import GameResult

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
    

class GameSession(db.Model):
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    tickets = db.Column(db.Integer, nullable=False, default=0)


class Game(db.Model):
    __tablename__ = "games"

    id = db.Column(db.Integer, primary_key=True)
    game_session_id = db.Column(db.Integer, db.ForeignKey("game_sessions.id"), nullable=False)
    game_result = db.Column(db.Enum(GameResult), default=GameResult.LOSE, nullable=False)
    game_time = db.Column(db.Integer)
    date = db.Column(db.DateTime, nullable=False)