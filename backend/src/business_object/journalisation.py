from __future__ import annotations
 
from datetime import datetime, timezone
from typing import Any
 

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

    def vers_dict(self) -> dict[str, Any]:
        """
        Convertit l'entrée en dictionnaire de types simples (str, int, bool)
        pour être écrite dans un fichier JSON ou une base de données.
        La date est convertie en texte au format ISO.
        """
        return {
            "id_utilisateur": self._id_utilisateur,
            "timestamp": self._timestamp.isoformat(),
            "score_vulnerabilite": self._score_vulnerabilite,
            "score_eco": self._score_eco,
            "decision": self._decision,
        }

    @classmethod
    def depuis_dict(cls, data: dict[str, Any]) -> Journalisation:
        """
        Recrée un objet Journalisation à partir d'un dictionnaire relu depuis le stockage (classe Historique).
        C'est l'opération inverse de to_dict().
        """
        return cls(
            id_utilisateur=data["id_utilisateur"],
            score_vulnerabilite=int(data["score_vulnerabilite"]),
            score_eco=int(data["score_eco"]),
            decision=bool(data["decision"]),
            timestamp=datetime.fromisoformat(data["timestamp"]),
        )

    def __eq__(self, autre: object) -> bool:
        if not isinstance(autre, Journalisation):
            return NotImplemented
        return self.vers_dict() == autre.vers_dict()
    
    def __hash__(self) -> int:
        return hash((self._id_utilisateur,
                     self._score_vulnerabilite,
                     self._score_eco,
                     self._decision,
                     self._timestamp.isoformat()))
 
    def __str__(self) -> str:
        statut = "Certifié" if self._decision else "Refusé"
        return (
            f"[{self._timestamp:%Y-%m-%d %H:%M}] {self._id_utilisateur} "
            f"vulnerabilite={self._score_vulnerabilite} eco={self._score_eco} -> {statut}"
        )