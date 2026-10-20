class FacteurEmissionPays:
    """ Référentiel des facteurs d'émission électrique
    par pays, consulté par CalculateurCO2.

    Attributes:
        facteurs_pays: dictionnaire {nom du pays: facteur d'émission en
            gCO2e/kWh} (dict[str, float]).

    """

    def __init__(self) -> None:
        self.facteurs_pays: dict[str, float] = {
            "France": 41,
            "Royaume-Uni": 217,
            "Irlande": 257,
            "Espagne": 154,
            "Portugal": 128,
            "Belgique": 150,
            "Pays-Bas": 254,
            "Danemark": 114,
            "Allemagne": 330,
            "Pologne": 589,
            "Norvege": 28,
        }

    def obtenir_facteur(self, pays: str) -> float:
        """Retourne le facteur d'émission électrique d'un pays.

        Args:
            pays: le nom du pays (doit être une clé de facteurs_pays).

        Returns:
            float: le facteur d'émission en gCO2e/kWh.

        """

        if pays not in self.facteurs_pays:
            raise ValueError(f"Pays inconnu : {pays}")
        return self.facteurs_pays[pays]
