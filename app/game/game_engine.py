from datetime import datetime

from app.models import db, Game, GameSession


class GameEngine():
    def __init__(self, session_id: int):
        self.game = self.initGame(session_id)
        self.board = [0 for i in range(9)]
        self.turn = 'x'


    def initGame(self, session_id: int) -> Game:
        new_game = Game(
            game_session_id=session_id,
            date = datetime.now().strftime("%Y/%m/%d")
        )
        db.session.add(new_game)
        db.session.commit()
        db.session.flush()

        return new_game
    
    
    def makeMove(self, square_id: int, player: str) -> bool:
        # if self.board[square_id] == 0 and self.turn == player:
        if self.board[square_id] == 0:
            self.board[square_id] = self.turn
            self.changeTurn()
            return True
        else:
            return False
        

    def changeTurn(self) -> None:
        if self.turn == 'x':
            self.turn = 'o'
        else:
            self.turn = 'x'


    def checkWinner(self):
        # Check rows
        for i in range(3):
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != 0:
                return self.board[i*3]
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != 0:
                return self.board[i]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != 0:
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != 0:
            return self.board[2]
        
        # Check draw
        if 0 not in self.board:
            return 'draw'
        
        return None