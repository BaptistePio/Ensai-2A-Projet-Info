import random
from typing import TYPE_CHECKING

from business_object.game import Game
from business_object.game_mode.GameMode import JeuStandard
from business_object.player import Player

if TYPE_CHECKING:
    from business_object.game import Game
    from business_object.player import Player

class CoinFlipMode(JeuStandard):
    def play(self, p1 : Player, p2 : Player, **kwags) -> Game:
        