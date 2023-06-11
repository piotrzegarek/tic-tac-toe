from app.game.game_logic import GameLogic

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Server(metaclass=Singleton):
    def __init__(self):
        self.games = {}

    def createGame(self, game_session_id, gamemode):
        if gamemode == 'singleplayer':
            game = GameLogic(game_session_id, gamemode)
            self.games[game.game.id] = game
            player = game.player1
        else:
            game = self.findFreeGame()
            if game == None:
                game = GameLogic(game_session_id, gamemode)
                self.games[game.game.id] = game
                player = game.player1
            else:
                player = game.player2

        return game, player
    

    def findFreeGame(self):
        for game_ids in self.games:
            game = self.games[game_ids]
            if game.mode == 'multiplayer' and game.player2 == None:
                game.addPlayer2()
                return game
        return None
    

    def getGame(self, game_id):
        return self.games.get(game_id)

    def deleteGame(self, game_id):
        del self.games[game_id]

server = Server()