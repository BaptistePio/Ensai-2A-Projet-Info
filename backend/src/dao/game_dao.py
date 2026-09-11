from dao.db_connection import DBConnection
from business_object.game import Game
from utils.log_utils import get_logger, log
from utils.singleton import Singleton
import logging

logger = logging.getLogger(__name__)


class GameDao(metaclass=Singleton):
    """Class containing methods to access Games in the database."""

    @log
    def create(self, game: Game) -> bool:
        """Create a game in the database.
        Args:
            Game to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO game(id_player1, id_player2, game_mode, id_winner, description, timestamp) VALUES "
                        "(%(id_player1)s, %(id_player2)s, %(game_mode)s, %(id_winner)s, %(description)s, %(timestamp)s) "
                        "RETURNING id_game;",
                        {
                            "id_player1": game.player1.id_player,
                            "id_player2": game.player2.id_player,
                            "game_mode": game.game_mode,
                            "id_winner": game.winner.id_player if game.winner else None,
                            "description": game.description,
                            "timestamp": game.timestamp,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            game.id_game = res["id_game"]
            created = True

        return created