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
        new_game = GameLogic(game_session_id, gamemode)
        self.games[new_game.game.id] = new_game

        return new_game

    def getGame(self, game_id):
        return self.games.get(game_id)

    def deleteGame(self, game_id):
        del self.games[game_id]

server = Server()