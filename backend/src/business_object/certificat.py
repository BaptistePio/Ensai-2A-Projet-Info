from __future__ import annotations

import json
from datetime import UTC, datetime

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


class Certificat:
    """
    Certificat d'attestation délivré lorsqu'un audit respecte la Quality Gate.
    Il est signé par le Verificateur (Ed25519) : la signature garantit que son
    contenu n'a pas été modifié depuis son émission.
    """

    STATUT_VALIDE = "Valide"

    # TODO(Audit): score_global : la règle de calcul sera décidée dans Audit.
    # TODO(Soumission): empreinte_code : format attendu = SHA-256 en hexadécimal, à confirmer
    #   avec la classe (Soumission ou Audit) qui la calcule.
    # TODO(Utilisateur): id_utilisateur est supposé de type str ; vérifier le type réel de
    #   Utilisateur.id_utilisateur.
    # TODO("Valide"): Faut-il générer un certificat m^me quand invalide (code à changer)

    def __init__(self, id_certificat: str, id_utilisateur: str, empreinte_code: str,
                 date_emission: datetime, status: str, score_global: int,
                 signature: bytes = b"") -> None:
        if status != self.STATUT_VALIDE:
            raise ValueError(f"status doit valoir exactement '{self.STATUT_VALIDE}'")
        self._id_certificat = id_certificat
        self._id_utilisateur = id_utilisateur
        self._empreinte_code = empreinte_code
        self._date_emission = date_emission
        self._status = status
        self._score_global = score_global
        self._signature = signature

    @property
    def id_certificat(self) -> str:
        return self._id_certificat

    @property
    def id_utilisateur(self) -> str:
        return self._id_utilisateur

    @property
    def empreinte_code(self) -> str:
        return self._empreinte_code

    @property
    def date_emission(self) -> datetime:
        return self._date_emission

    @property
    def status(self) -> str:
        return self._status

    @property
    def score_global(self) -> int:
        return self._score_global

    @property
    def signature(self) -> bytes:
        return self._signature

    @signature.setter
    def signature(self, valeur: bytes) -> None:
        # Verificateur.signer_certificat() renseigne la signature après la création
        self._signature = valeur

    def message_a_signer(self) -> bytes:
        """
        Contenu signé par le Verificateur : tous les champs sauf la signature,
        sérialisés de façon stable (clés triées, date normalisée en UTC).
        """
        date = self._date_emission
        if date.tzinfo is not None:
            date = date.astimezone(UTC)
        contenu = {
            "id_certificat": self._id_certificat,
            "id_utilisateur": self._id_utilisateur,
            "empreinte_code": self._empreinte_code,
            "date_emission": date.isoformat(),
            "status": self._status,
            "score_global": self._score_global,
        }
        return json.dumps(contenu, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False).encode("utf-8")

    def verifier_authenticite(self, cle_publique_signature: bytes) -> bool:
        """
        Vérifie que la signature correspond au contenu actuel du certificat, avec
        Verificateur.cle_publique_signature (et non sa cle_publique, qui sert à l'ECDH).
        Renvoie False si le certificat n'est pas signé ou a été modifié.
        """
        if not self._signature:
            return False
        try:
            Ed25519PublicKey.from_public_bytes(cle_publique_signature).verify(
                self._signature, self.message_a_signer())
        except (InvalidSignature, ValueError):
            return False
        return True