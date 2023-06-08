from app.models import db, Game
from datetime import datetime

class GameEngine():
    def __init__(self, session_id: int):
        self.game = self.initGame(session_id)
        self.board = [[0 for _ in range(3)] for _ in range(3)]

    def initGame(self, session_id: int):
        new_game = Game(
            game_session_id=session_id,
            date = datetime.now().strftime("%Y/%m/%d")
        )
        db.session.add(new_game)
        db.session.commit()
        db.session.flush()

        return new_game
    