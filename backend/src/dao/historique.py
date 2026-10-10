from __future__ import annotations

from datetime import datetime
from business_object.journalisation import Journalisation
from dao.connexion_bdd_ex import get_connection 

class Historique:
    """
    Classe (DAO) permettant de gérer, d'enregistrer et de retrouver les entrées 
    de journal stockées (via Journalisation) de manière persistante dans une base de données SQL.
    """

    def __init__(self) -> None:
        pass

    def enregistrer_journal(self, id_utilisateur: str, timestamp: datetime | None,
                            score_vulnerabilite: int, score_eco: int,
                            decision: bool) -> None:
        """
        Enregistre de façon persistante les résultats d'un audit en base de données.
        """
        entree = Journalisation(id_utilisateur, score_vulnerabilite, score_eco,
                        decision, timestamp)
        requete = """
            INSERT INTO journalisation 
            (id_utilisateur, timestamp, score_vulnerabilite, score_eco, decision)
            VALUES (%s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(requete, (
                    entree.id_utilisateur,
                    entree.timestamp,
                    entree.score_vulnerabilite,
                    entree.score_eco,
                    entree.decision
                    ))
                conn.commit()

    def trouver_utilisateur(self, id_utilisateur: str) -> list[Journalisation]:
        """
        Récupère les entrées d'un utilisateur.
        """
        requete = """
            SELECT id_utilisateur, score_vulnerabilite, score_eco, decision, timestamp 
            FROM journalisation 
            WHERE id_utilisateur = %s
            ORDER BY timestamp DESC
        """
        return self.transfo_sql_en_journalisation(requete, (id_utilisateur,))

    def trouver_periode(self, debut: datetime, fin: datetime) -> list[Journalisation]:
        """
        Récupère les entrées entre deux dates.
        """
        requete = """
            SELECT id_utilisateur, score_vulnerabilite, score_eco, decision, timestamp
            FROM journalisation 
            WHERE timestamp BETWEEN %s AND %s
            ORDER BY timestamp ASC
        """
        return self.transfo_sql_en_journalisation(requete, (debut, fin))

    def repertorier_statut(self, certifie: bool) -> list[Journalisation]:
        """
        Récupère les audits par statut.
        """
        requete = """
            SELECT id_utilisateur, score_vulnerabilite, score_eco, decision, timestamp 
            FROM journalisation 
            WHERE decision = %s
        """
        return self.transfo_sql_en_journalisation(requete, (certifie,))

    def transfo_sql_en_journalisation(self, requete: str, parametres: tuple) -> list[Journalisation]:
        """
        Méthode utilitaire pour transformer les lignes PostgreSQL en objets Journalisation.
        Fais correspondre une donnée brute (tuple issu de la base de données) et un objet
        de la classe Journalisation
        """
        results = []
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(requete, parametres)
                rows = cursor.fetchall()
                for row in rows:
                    results.append(Journalisation(
                        id_utilisateur=row[0],
                        score_vulnerabilite=row[1],
                        score_eco=row[2],
                        decision=row[3],
                        timestamp=row[4]
                    ))
        return results