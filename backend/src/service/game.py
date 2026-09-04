from datetime import datetime 
from business_object.player import Player

class Game:

    def __init__(self,id_game, Player1: Player, Player2: Player, game_mode, winner, description, timestamp):
        self.id_game = None
        self.Player1 = Player1
        self.Player2 = Player2
        self.game_mode = game_mode
        self.winner = winner
        self.description = description
        self.timestamp = timestamp

    def __str__(self):
            return f"Game({self.game_mode} betwenn {self.Player1} and {self.Player2}, winner: {self.winner})"
