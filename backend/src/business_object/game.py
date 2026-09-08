from datetime import datetime
from backend.src.business_object.player import Player


class Game:
    def __init__(
        self,
        player1: Player,
        player2: Player,
        game_mode: str,
        description: str,
        winner=None,
        timestamp=None,
    ):
        """
        Initialise une nouvelle instance de Game.

        :param player1: L'objet Player du premier joueur.
        :param player2: L'objet Player du second joueur.
        :param game_mode: Le type de jeu (« pile ou face » ou « dés »).
        :param description: Détails textuels sur la partie.
        :param winner: L'objet Player du vainqueur, ou None en cas d'égalité.
        :param timestamp: Date de la partie (si None, utilise datetime.now()).
        """
        # L'identifiant est None car il sera généré par la base de données
        self.id_game = None

        # Attributs obligatoires
        self.player1 = player1
        self.player2 = player2
        self.game_mode = game_mode
        self.description = description

        # Attributs optionnels
        self.winner = winner 
        self.timestamp = timestamp if timestamp else datetime.now()

    def __str__(self) -> str:
        """Retourne une représentation lisible du jeu."""
        if self.winner:
            return f"{self.game_mode} entre {self.player1.username} et {self.player2.username}. Gagnante : {self.winner.username}"
        
        return f"{self.game_mode} entre {self.player1.username} et {self.player2.username}."