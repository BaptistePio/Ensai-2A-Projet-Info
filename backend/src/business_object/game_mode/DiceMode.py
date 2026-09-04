import random
from typing import TYPE_CHECKING

from business_object.game import Game
from business_object.player import Player
from business_object.game_mode.GameMode import JeuStandard 

if TYPE_CHECKING:
    from business_object.game import Game
    from business_object.player import Player


class DiceMode(JeuStandard):

    def play(self, p1: Player, p2: Player, **kwargs) -> Game:
        """
        Crée le jeu de dés
        """
        dice_p1 = random.randint(1,6)
        dice_p2 = random.randint(1,6)

        if dice_p1 > dice_p2 :
            winner = p1
        elif dice_p1 < dice_p2 :
            winner = p2
        else :
            None

        print(f"Player 1 ({p1.name}) lance : {dice_p1}")
        print(f"Player 2 ({p2.name}) lance : {dice_p2}")

        description = f"Score {dice_p1} et {dice_p2}"

        return Game(
            player1 = p1,
            player2 = p2,
            game_mode = "lancé de dés",
            description = description,
            winner = winner
        )

