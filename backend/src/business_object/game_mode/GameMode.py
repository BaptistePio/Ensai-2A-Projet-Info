from abc import ABC, abstractmethod
from typing import Type, Union

from business_object.game import Game
from business_object.player import Player
from business_object.game_mode import CoinFlipMode
from business_object.game_mode import DiceMode


class JeuStandard(ABC):

    @abstractmethod
    def play(self, p1: Player, p2: Player, **kwargs) -> Game:
        """
        Crée les deux joueurs
        Prends deux joueurs et retourne une instance de jeu
        """
        pass

class GameModeFactory:

    @classmethod
    def get_mode(cls,game_mode: str) -> Game:
        """
        Returns the corresponding GameMode object.
        Args:
            game_mode (str): The identifier of the game mode (e.g., 'coinflip', 'dice').
        Returns:
            GameMode: An instance of a class implementing GameMode.
        Raises:
            ValueError: If the requested game_mode is not supported.
        """
        if game_mode == "coinflip":
            return CoinFlip()
        elif game_mode == "lancé de dés":
            return DiceMode()
        else:
            raise ValueError(f"Le jeu {game_mode} n'existe pas")
