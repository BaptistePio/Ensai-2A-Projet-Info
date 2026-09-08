import os


class ScoringStrategy:
    @classmethod
    def calculate_expected_score(cls, elo_a, elo_b) -> float:
        """Calculates the probability of player A winning against player B.
        Args:
            elo_a (float): The current Elo rating of first player.
            elo_b (float): The current Elo rating of second player.

        Returns:
            float: The expected score for player 1 (between 0 and 1).
        """
        return 1 / (1 + 10 ** ((elo_b - elo_a) / 400))

    @classmethod
    def calculate_new_ratings(cls, elo_a, elo_b, player_a_won: bool) -> tuple[int, int]:
        """Computes the new Elo ratings for two players after a match.
        Args:
            elo_a (float): Current Elo of player 1.
            elo_b (float): Current Elo of player 2.
            player_a_won (bool): True if player 1 won, False if player 2 won.
        Returns:
            tuple[int, int]: A tuple containing (new_elo1, new_elo2).
        """
        k_factor = int(os.environ["ELO_K_FACTOR"])

        score_a = 1.0 if player_a_won else 0.0
        score_b = 1.0 - score_a

        new_elo_a = round(elo_a + k_factor * (score_a - cls.calculate_expected_score(elo_a, elo_b)))
        new_elo_b = round(elo_b + k_factor * (score_b - cls.calculate_expected_score(elo_b, elo_a)))

        return new_elo_a, new_elo_b

    @classmethod
    def update_player_ratings(cls, game: 'Game'):
        """
        Calculates and updates the elo attributes of the players within a game.
        No update if there is no winner (Draw).
        
        :param game: The Game object containing player1, player2, and winner.
        """
        # Si pas de vainqueur (égalité), on ne fait rien
        if not game.winner:
            return

        # On extrait les informations directement de l'objet game
        p1 = game.player1
        p2 = game.player2
        winner = game.winner

        # On calcule les nouveaux scores
        # On vérifie si le vainqueur est le joueur 1
        is_p1_winner = (p1 == winner)
        
        new_elo1, new_elo2 = cls.calculate_new_ratings(
            p1.elo, 
            p2.elo, 
            player_a_won=is_p1_winner
        )

        # On met à jour les attributs des objets joueurs
        p1.elo = new_elo1
        p2.elo = new_elo2