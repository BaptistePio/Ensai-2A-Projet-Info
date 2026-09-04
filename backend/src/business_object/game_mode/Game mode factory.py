from business_object.game_mode import GameMode
from business_object.player import Player


class GameModeFactory:

    @classmethod
    def get_mode(cls, game_mode: str) -> GameMode:
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
            return  GameMode.game_mode

        elif game_mode == "dicemode":
            return GameMode.game_mode

        else:
            raise ValueError("le mode de jeu demandé ne peut pas etre supporté")