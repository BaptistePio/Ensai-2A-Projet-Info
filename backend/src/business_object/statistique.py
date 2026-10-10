from __future__ import annotations

from datetime import date, timezone

from business_object.journalisation import Journalisation


class Statistique:
    """
    Résume les audits d'un utilisateur à partir de ses entrées de journal
    (Journalisation) comprenant: nombre de soumissions, score moyen par type, et activité
    par jour.
    """

    def __init__(self, id_utilisateur: str, nb_soumissions: int,
                 score_vulnerabilite_moyen: float, score_eco_moyen: float,
                 activite_par_jour: dict[date, int] | None = None) -> None:
        if not id_utilisateur:
            raise ValueError("id_utilisateur ne peut pas être vide")
        if nb_soumissions < 0 or score_vulnerabilite_moyen < 0 or score_eco_moyen < 0:
            raise ValueError("les soumissions de code et les scores moyens doivent être positifs ou nuls")

        self._id_utilisateur = id_utilisateur
        self._nb_projet = nb_soumissions
        self._score_vulnerabilite_moyen = score_vulnerabilite_moyen
        self._score_eco_moyen = score_eco_moyen
        self._activite_par_jour = dict(activite_par_jour or {})

    @property
    def id_utilisateur(self) -> str:
        return self._id_utilisateur

    @property
    def nb_soumissions(self) -> int:
        return self._nb_soumissions

    @property
    def score_vulnerabilite_moyen(self) -> float:
        return self._score_vulnerabilite_moyen

    @property
    def score_eco_moyen(self) -> float:
        return self._score_eco_moyen

    @property
    def activite_par_jour(self) -> dict[date, int]:
        """Nombre de soumissions par jour"""
        return dict(sorted(self._activite_par_jour.items()))

    @classmethod
    def obtenir_statistiques(cls, id_utilisateur: str,
                             entrees: list[Journalisation]) -> Statistique:
        """
        Calcule les statistiques d'un utilisateur à partir de ses entrées de journal
        Chaque entrée compte pour une soumission. 
        Les jours sont ceux de la date UTC (s'adapte à la zone où l'utilisateur se trouve).
        Sans entrée, tout vaut 0 (et l'activité est vide).
        """
        for entree in entrees:
            if entree.id_utilisateur != id_utilisateur:
                raise ValueError(
                    f"L'entrée de {entree.id_utilisateur} n'appartient pas à {id_utilisateur}"
                )

        activite: dict[date, int] = {}
        for entree in entrees:
            instant = entree.timestamp
            if instant.tzinfo is not None:
                instant = instant.astimezone(timezone.utc)
            jour = instant.date()
            activite[jour] = activite.get(jour, 0) + 1

        if not entrees:
            return cls(id_utilisateur, 0, 0.0, 0.0, activite)

        n = len(entrees)
        return cls(
            id_utilisateur,
            n,
            sum(e.score_vulnerabilite for e in entrees) / n,
            sum(e.score_eco for e in entrees) / n,
            activite,
        )

    def _cle(self) -> tuple:
        return (self._id_utilisateur, self._nb_projet, self._score_vulnerabilite_moyen,
                self._score_eco_moyen, tuple(sorted(self._activite_par_jour.items())))

    def __eq__(self, autre: object) -> bool:
        if not isinstance(autre, Statistique):
            return NotImplemented
        return self._cle() == autre._cle()

    def __hash__(self) -> int:
        return hash(self._cle())

    def __str__(self) -> str:
        return (f"Statistiques de : {self.id_utilisateur} : "
                f"Nombre de soumission(s): {self._nb_projet}, "
                f"vulnérabilité moyenne : {self._score_vulnerabilite_moyen:.2f}, "
                f"éco moyen : {self._score_eco_moyen:.2f}")