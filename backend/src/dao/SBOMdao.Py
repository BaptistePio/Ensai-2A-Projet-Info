# Comment insérer une ligne dans notre table sbom. Chaque ligne reprèsente un sbom bien défini. (pour la sauvegarde.)
# Recupérer un sbom lié à un audit.
# Recupérer un sbom à partir de son identifiant.
from business_object.SBOM import SBOM
from dao.connexion_bdd_ex import get_connection


class SBOMDao:
    """Gère les échanges entre les objets SBOM et PostgreSQL."""

    def __init__(self) -> None:
        """Initialise le DAO."""
        pass

    def sauvegarder(self, sbom: SBOM) -> None:
        """Enregistre un SBOM dans la base de données."""
        requete = """
            INSERT INTO sbom (
                id_audit,
                contenu,
                date_generation,
                format
            )
            VALUES (%s, %s, %s, %s)
        """

        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    requete,
                    (
                        sbom.id_audit,
                        sbom.contenu,
                        sbom.date_generation,
                        sbom.format,
                    ),
                )
            conn.commit()

    def recuperer_par_audit(self, id_audit: int) -> list[SBOM]:
        """Récupère les SBOM associés à un audit."""
        requete = """
            SELECT id_sbom, id_audit, contenu,
                   date_generation, format
            FROM sbom
            WHERE id_audit = %s
            ORDER BY date_generation DESC
        """

        return self._execute_and_map(requete, (id_audit,))

    def recuperer_par_id(self, id_sbom: int) -> SBOM | None:
        """Récupère un SBOM à partir de son identifiant."""
        requete = """
            SELECT id_sbom, id_audit, contenu,
                   date_generation, format
            FROM sbom
            WHERE id_sbom = %s
        """

        resultats = self._execute_and_map(requete, (id_sbom,))

        if not resultats:
            return None

        return resultats[0]

    def _execute_and_map(
        self,
        requete: str,
        params: tuple,
    ) -> list[SBOM]:
        """Exécute une requête et convertit les lignes en objets SBOM."""
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(requete, params)
                lignes = cursor.fetchall()

        resultats = []

        for ligne in lignes:
            resultats.append(
                SBOM(
                    id_sbom=ligne[0],
                    id_audit=ligne[1],
                    contenu=ligne[2],
                    date_generation=ligne[3],
                    format=ligne[4],
                )
            )

        return resultats
