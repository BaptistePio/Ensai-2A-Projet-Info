from abc import ABC, abstractmethod
from backend.src.business_object.player import Player
from backend.src.business_object.game import Game


class GameMode(ABC):
    """
    Classe de base abstraite pour définir un mode de jeu.
    """

    @abstractmethod
    def play(self, p1: Player, p2: Player, **kwargs) -> Game:
        """
        Exécute une partie de jeu standard.

        :param p1: Le premier joueur.
        :param p2: Le second joueur.
        :return: Un objet Game contenant les résultats de la partie.
        """
        pass
