class GameDao(metaclass=Singleton):

    def create(self, player) -> bool:
        """Create a player in the database.
        Args:
            Player to create
        Returns:
            True if creation is successful, False otherwise
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO player(username, password, elo, email, pokemon_fan) VALUES "
                        "(%(username)s, %(password)s, %(elo)s, %(email)s, %(pokemon_fan)s) "
                        "RETURNING id_player;",
                        {
                            "username": player.username,
                            "password": player.password,
                            "elo": player.elo,
                            "email": player.email,
                            "pokemon_fan": player.pokemon_fan,
                        },
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logger.error(e)
            raise

        created = False
        if res:
            player.id_player = res["id_player"]
            created = True

        return created