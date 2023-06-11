import random
import time
from datetime import datetime

from app.models import db, Game, GameSession
from app.enums import GameResult

class GameLogic():
    def __init__(self, session_id: int, mode: str):
        self.games = [self.initGame(session_id)]
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
            self.player2 = None


    def addPlayer2(self, game_session_id: int):
        self.player2 = 'x' if self.player1 == 'o' else 'o'
        self.games.append(self.initGame(game_session_id))


    def initGame(self, session_id: int) -> Game:
        new_game = Game(
            game_session_id=session_id,
        )
        db.session.add(new_game)
        db.session.commit()
        db.session.flush()

        return new_game


    def endGame(self) -> None:
        if self.winner == self.player1:
            result = [GameResult.WIN, GameResult.LOSE]
        elif self.winner == 'draw':
            result = [GameResult.DRAW, GameResult.DRAW]
        else:
            result = [GameResult.LOSE, GameResult.WIN]

        game_time = (datetime.now() - self.time).total_seconds()
        for ind, game in enumerate(self.games):
            game_obj = Game.query.filter_by(id=game.id).first()
            game_obj.game_time = game_time
            game_session = GameSession.query.filter_by(id=game.game_session_id).first()
            game_obj.tickets_after = game_session.tickets
            game_obj.game_result = result[ind]
        db.session.commit()
        

    def makeMove(self, square_id: int, player: str) -> bool:
        if self.board[square_id] == 0 and self.turn == player:
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
            print('draw')
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