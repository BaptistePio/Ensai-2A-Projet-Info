from abc import ABC, abstractmethod

from business_object.game import Game
from business_object.player import Player


class JeuStandard(ABC):

    @abstractmethod
    def play(self, p1: Player, p2: Player, **kwargs) -> Game:
        """
        Crée les deux joueurs
        Prends deux joueurs et retourne une instance de jeu
        """
        pass
