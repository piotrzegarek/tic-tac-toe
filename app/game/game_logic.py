import random
import time
from datetime import datetime

from app.models import db, Game, GameSession
from app.enums import GameResult

class GameLogic():
    def __init__(self, session_id: int, mode: str):
        self.game = self.initGame(session_id)
        self.board = [0 for i in range(9)]
        self.turn = 'x'
        self.time = datetime.now()
        self.winner = None
        self.mode = mode
        self.initPlayers()


    def initPlayers(self):
        self.player1 = random.choice(['x', 'o'])
        player2 = 'x' if self.player1 == 'o' else 'o'
        if self.mode == 'singleplayer':
            self.player2 = ComputerPlayer(player2)
            if player2 == self.turn:
                self.makeMove(self.player2.generateMove(self.board), self.player2.player)
        else:
            # TODO: Add multiplayer
            pass


    def initGame(self, session_id: int) -> Game:
        new_game = Game(
            game_session_id=session_id,
        )
        db.session.add(new_game)
        db.session.commit()
        db.session.flush()

        return new_game


    def endGame(self) -> None:
        self.game.game_time = (datetime.now() - self.time).total_seconds()
        if self.winner == self.player1:
            self.game.game_result = GameResult.WIN
        elif self.winner == 'draw':
            self.game.game_result = GameResult.DRAW
        else:
            self.game.game_result = GameResult.LOSE
        game = Game.query.filter_by(id=self.game.id).first()
        game.game_result = self.game.game_result
        game.game_time = self.game.game_time
        db.session.commit()
        

    def makeMove(self, square_id: int, player: str) -> bool:
        if self.board[square_id] == 0 and self.turn == player:
        # if self.board[square_id] == 0:
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
                self.winner = self.board[i*3]
                return self.board[i*3]
        # Check columns
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != 0:
                self.winner = self.board[i]
                return self.board[i]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != 0:
            self.winner = self.board[0]
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != 0:
            self.winner = self.board[2]
            return self.board[2]
        
        # Check draw
        if 0 not in self.board:
            self.winner = 'draw'
            return 'draw'
        
        return None
    

class ComputerPlayer():
    def __init__(self, player: str):
        self.player = player
    
    def generateMove(self, board: list) -> int:
        time.sleep(1)
        board_options = self.getOptions(board)
        
        return random.choice(board_options)

    def getOptions(self, board: list) -> list:
        return [i for i, x in enumerate(board) if x == 0]