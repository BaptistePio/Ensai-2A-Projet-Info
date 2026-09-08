import random
from typing import Optional
from backend.src.business_object.game_mode import GameMode
from backend.src.business_object.player import Player


class CoinFlipMode(GameMode):
    def play(self, p1: Player, p2: Player, **kwargs) -> "Game":
        # On extrait 'choix' des kwargs. On met une valeur par défaut au cas où.
        choix = kwargs.get("choix", "pile")

        resultat = random.choice(["pile", "face"])

        winner: Optional[Player] = None
        if choix.lower() == resultat:
            winner = p1
        else:
            winner = p2

        description = f"Le résultat était : {resultat}."

        from backend.src.business_object.game import Game

        return Game(
            player1=p1, player2=p2, game_mode="Pile ou face", description=description, winner=winner
        )
