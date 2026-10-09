
from datetime import datetime


class SBOM:
    """Représente un SBOM (Software Bill of Materials).

    Attributes:
        id_sbom (int): Identifiant unique du SBOM.
        id_audit (int): Identifiant de l'audit à l'origine du SBOM.
        contenu (str): Contenu du SBOM généré.
        date_generation (datetime): Date et heure de génération du SBOM.
        format (str): Format du SBOM, par exemple JSON ou XML.
    """

    def __init__(
        self,
        id_sbom: int,
        id_audit: int,
        contenu: str,
        date_generation: datetime,
        format: str,
    ) -> None:
        """Initialise un SBOM avec ses attributs."""
        self.id_sbom = id_sbom
        self.id_audit = id_audit
        self.contenu = contenu
        self.date_generation = date_generation
        self.format = format

    def __str__(self) -> str:
        """Renvoie une description lisible du SBOM."""
        return (
            f"SBOM n°{self.id_sbom}, audit n°{self.id_audit}, "
            f"format {self.format}, généré le "
            f"{self.date_generation:%d/%m/%Y à %H:%M}"
        )

    def __repr__(self) -> str:
        """Renvoie une représentation détaillée du SBOM."""
        return (
            f"SBOM(id_sbom={self.id_sbom!r}, "
            f"id_audit={self.id_audit!r}, "
            f"contenu={self.contenu!r}, "
            f"date_generation={self.date_generation!r}, "
            f"format={self.format!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare deux SBOM selon leurs attributs."""
        if not isinstance(other, SBOM):
            return NotImplemented

        return (
            self.id_sbom == other.id_sbom
            and self.id_audit == other.id_audit
            and self.contenu == other.contenu
            and self.date_generation == other.date_generation
            and self.format == other.format
        )
