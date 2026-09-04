import random
from typing import TYPE_CHECKING

from business_object.game import Game
from business_object.player import Player
from business_object.game_mode.GameMode import JeuStandard 

if TYPE_CHECKING:
    from business_object.game import Game
    from business_object.player import Player