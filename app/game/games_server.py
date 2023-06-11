from app.game.game_logic import GameLogic

class Singleton(type):
    """ Singleton metaclass. """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Server(metaclass=Singleton):
    """ Server class for handling currently played games. """
    def __init__(self):
        self.games = {}

    def createGame(self, game_session_id: int, gamemode: str) -> tuple:
        """ Create new game and add it to the list of games. """
        if gamemode == 'singleplayer':
            game = GameLogic(game_session_id, gamemode)
            self.games[game.games[0].id] = game
            player = game.player1
        else:
            game = self.findFreeGame(game_session_id)
            if game == None:
                game = GameLogic(game_session_id, gamemode)
                self.games[game.games[0].id] = game
                player = game.player1
            else:
                player = game.player2

        return game, player
    

    def findFreeGame(self, game_session_id: int):
        """ Find game for multiplayer with player 2 free spot. """
        for game_ids in self.games:
            game = self.games[game_ids]
            if game.mode == 'multiplayer' and game.player2 == None:
                game.addPlayer2(game_session_id)
                return game
        return None
    

    def getGame(self, game_id: int) -> GameLogic:
        """ Get game by id from the server. """
        return self.games.get(game_id)


    def deleteGame(self, game_id: int) -> None:
        """ Delete game by id from the server. """
        del self.games[game_id]

server = Server()