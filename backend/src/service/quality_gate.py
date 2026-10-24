from __future__ import annotations

import uuid
from datetime import UTC, datetime

from business_object.certificat import Certificat


class CertificatRefuse(Exception):
    """Levée quand la Quality Gate refuse un audit : aucun certificat n'est délivré."""


class QualityGate:
    """
    Décide si un audit est acceptable en fonction du niveau de vulnérabilité et de l'empreinte
    carbone.
    A la suite de cette évaluation, on génère le certificat d'attestation (non signé) lorsque
    l'audit est accepté ; la signature est ajoutée ensuite par Verificateur.signer_certificat().
    """

    def __init__(self, seuil_vulnerabilite_max: int, seuil_carbone_max: int) -> None:
        if seuil_vulnerabilite_max < 0 or seuil_carbone_max < 0:
            raise ValueError("Les seuils doivent être positifs ou nuls")

        self._seuil_vulnerabilite_max = seuil_vulnerabilite_max
        self._seuil_carbone_max = seuil_carbone_max

    @property
    def seuil_vulnerabilite_max(self) -> int:
        return self._seuil_vulnerabilite_max

    @property
    def seuil_carbone_max(self) -> int:
        return self._seuil_carbone_max

    def evaluer(self, score_vulnerabilite: int, score_eco: int) -> bool:
        """
        Renvoie True (certificat possible) si les deux scores sont inférieurs ou égaux
        à leur seuil maximal, et False (refus) dès que l'un des deux le dépasse.
        """
        if score_vulnerabilite < 0 or score_eco < 0:
            raise ValueError("Les scores doivent être positifs ou nuls")
        return (score_vulnerabilite <= self._seuil_vulnerabilite_max
                and score_eco <= self._seuil_carbone_max)

    def generer_certificat(self, id_utilisateur: str, empreinte_code: str,
                           score_vulnerabilite: int, score_eco: int,
                           score_global: int) -> Certificat:
        """
        Délivre un certificat NON SIGNÉ si l'audit respecte les seuils.
        Lève CertificatRefuse sinon (distincte de ValueError, qui signale des scores invalides).

        # TODO(Audit): score_global est reçu en paramètre car sa règle de calcul sera
        #   décidée dans Audit, une fois cette classe codée. Ne pas l'inventer ici.
        # TODO(Audit): Audit devra, autour de cet appel : (1) fournir id_utilisateur et
        #   calculer empreinte_code à partir de la Soumission, (2) appeler
        #   Verificateur.signer_certificat(certificat) sur le résultat, (3) attraper
        #   CertificatRefuse et enregistrer decision=False dans Journalisation.
        # TODO(persistance): aucune classe du diagramme ne stocke les certificats.
        #   id_certificat est généré ici (uuid4) mais pourrait venir de la base de données.
        """
        if not self.evaluer(score_vulnerabilite, score_eco):
            raise CertificatRefuse(
                f"Audit refusé : vulnérabilité {score_vulnerabilite} "
                f"(max {self._seuil_vulnerabilite_max}), "
                f"carbone {score_eco} (max {self._seuil_carbone_max})")

        return Certificat(
            id_certificat=str(uuid.uuid4()),
            id_utilisateur=id_utilisateur,
            empreinte_code=empreinte_code,
            date_emission=datetime.now(UTC),
            status=Certificat.STATUT_VALIDE,
            score_global=score_global,
        )