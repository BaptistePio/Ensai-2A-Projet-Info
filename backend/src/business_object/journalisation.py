from __future__ import annotations
 
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
 
 
@dataclass(frozen=True)
class Journalisation:
    """
    Rédige les éléments de l'Audit permettant de donner la décision 
    (classe les métadonnées mais n'enregistre aucun code)
    Une fois écrite, une entrée de journal ne peut plus être modifiée.
    """
    def __init__(self, id_utilisateur: str, score_vulnerabilite: int, score_eco: int, decision: bool, timestamp: datetime | None = None) -> None:
        if not id_utilisateur:
            raise ValueError("id_utilisateur ne peut pas être vide")
        if score_vulnerabilite < 0 or score_eco < 0:
            raise ValueError("Les scores doivent être positifs ou nuls")
 
        self._id_utilisateur = id_utilisateur
        self._score_vulnerabilite = score_vulnerabilite
        self._score_eco = score_eco
        self._decision = decision
        self._timestamp = timestamp or datetime.now(timezone.utc)

    @property
    def id_utilisateur(self) -> str:
        return self._id_utilisateur
 
    @property
    def score_vulnerabilite(self) -> int:
        return self._score_vulnerabilite
 
    @property
    def score_eco(self) -> int:
        return self._score_eco
 
    @property
    def decision(self) -> bool:
        return self._decision
 
    @property
    def timestamp(self) -> datetime:
        return self._timestamp