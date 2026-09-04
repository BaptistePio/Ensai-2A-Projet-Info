from datetime import datetime

from business_object.player import Player


class Game:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        game_mode: str,
        description: str,
        winner: Player | None = None,
        timestamp: datetime | None = None
    ):
        """
        Initialise une nouvelle instance de Game.

        :param player1: Le premier joueur (objet Player)
        :param player2: Le second joueur (objet Player)
        :param game_mode: Type de jeu ("pile ou face" ou "dés")
        :param description: Détails supplémentaires sur la partie
        :param winner: Le joueur gagnant (objet Player) ou None en cas d'égalité/en cours
        :param timestamp: Date et heure de la partie (par défaut l'heure actuelle)
        """
        self.id_game: int | None = None  # Sera renseigné par la base de données
        self.player1: Player = player1
        self.player2: Player = player2
        self.game_mode: str = game_mode
        self.winner: Player | None = winner
        self.description: str = description
        self.timestamp: datetime = timestamp if timestamp else datetime.now()

    def __str__(self) -> str:
        winner_name = self.winner.name if self.winner else "Aucun (Égalité ou en cours)"
        return (f"Mode: {self.game_mode} | "
                f"Entre: {self.player1.name} et {self.player2.name} | "
                f"Winner: {winner_name} | ")

# Exemple d'utilisation :
if __name__ == "__main__":
    p1 = Player("Alice")
    p2 = Player("Bob")


    game1 = Game(p1, p2, "dés", "Partie intense avec beaucoup de six !", winner=p1)
    print(game1)

    game2 = Game(p1, p2, "pile ou face", "Match nul")
    print(game2)