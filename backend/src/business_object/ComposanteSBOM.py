
class ComposanteSBOM:
    """Représente une composante logicielle d'un SBOM.

    Attributes:
        nom (str): Nom de la composante logicielle.
        version (str): Version de la composante.
        licence (str): Licence associée à la composante.
        hash_integrite (str): Empreinte cryptographique permettant
            de vérifier l'intégrité de la composante.
    """

    def __init__(
        self,
        nom: str,
        version: str,
        licence: str,
        hash_integrite: str,
    ) -> None:
        """Initialise une composante logicielle."""
        self.nom = nom
        self.version = version
        self.licence = licence
        self.hash_integrite = hash_integrite

    def __str__(self) -> str:
        """Renvoie une description lisible de la composante."""
        return (
            f"{self.nom} (version {self.version}, "
            f"licence {self.licence})"
        )

    def __repr__(self) -> str:
        """Renvoie une représentation détaillée de la composante."""
        return (
            f"ComposanteSBOM(nom={self.nom!r}, "
            f"version={self.version!r}, "
            f"licence={self.licence!r}, "
            f"hash_integrite={self.hash_integrite!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Compare deux composantes selon leurs attributs."""
        if not isinstance(other, ComposanteSBOM):
            return NotImplemented

        return (
            self.nom == other.nom
            and self.version == other.version
            and self.licence == other.licence
            and self.hash_integrite == other.hash_integrite
        )
