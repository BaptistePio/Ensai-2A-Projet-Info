from backend.src.business_object.game_mode import GameMode
from backend.src.business_object.dice_mode import DiceMode
from backend.src.business_object.coin_flip_mode import CoinFlipMode


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
        # On normalise la chaîne pour éviter les erreurs de casse (majuscules/minuscules)
        mode_key = game_mode.lower().strip()

        if mode_key == "dice":
            return DiceMode()

        elif mode_key == "coinflip" or mode_key == "pile ou face":
            return CoinFlipMode()

        else:
            raise ValueError(f"Le mode de jeu '{game_mode}' n'est pas supporté.")
