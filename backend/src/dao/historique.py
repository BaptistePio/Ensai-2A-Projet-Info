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
        temps = timestamp if timestamp is not None else datetime.now()
        requete = """
            INSERT INTO journalisation 
            (id_utilisateur, timestamp, score_vulnerabilite, score_eco, decision)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (
                    id_utilisateur, 
                    temps, 
                    score_vulnerabilite, 
                    score_eco, 
                    decision
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
        return self._execute_and_map(query, (id_utilisateur,))

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
        return self._execute_and_map(query, (debut, fin))

    def repertorier_statut(self, certifie: bool) -> list[Journalisation]:
        """
        Récupère les audits par statut.
        """
        requete = """
            SELECT id_utilisateur, score_vulnerabilite, score_eco, decision, timestamp 
            FROM journalisation 
            WHERE decision = %s
        """
        return self._execute_and_map(query, (certifie,))

    def _execute_and_map(self, query: str, params: tuple) -> list[Journalisation]:
        """
        Méthode utilitaire pour transformer les lignes PostgreSQL en objets Journalisation.
        """
        results = []
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                for row in rows:
                    # PostgreSQL renvoie directement les objets datetime et bool
                    results.append(Journalisation(
                        id_utilisateur=row[0],
                        score_vulnerabilite=row[1],
                        score_eco=row[2],
                        decision=row[3],
                        timestamp=row[4]
                    ))
        return results
2. Les changements clés à noter :