import random
from typing import Optional
from backend.src.business_object.game_mode import GameMode
from backend.src.business_object.player import Player


class DiceMode(GameMode):
    def play(self, p1: Player, p2: Player, **kwargs) -> "Game":
        score1 = random.randint(1, 6)
        score2 = random.randint(1, 6)

        winner = None
        if score1 > score2:
            winner = p1
        elif score2 > score1:
            winner = p2

        description = f"Joueur 1: {score1}, Joueur 2: {score2}."

        from backend.src.business_object.game import Game

        return Game(player1=p1, player2=p2, game_mode="Dés", description=description, winner=winner)
