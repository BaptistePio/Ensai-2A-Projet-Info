from facteur_emission_pays import FacteurEmissionPays


class CalculateurCO2:
    """Convertit l'énergie estimée (kWh) en émissions de CO2 (gCO2), selon le mix électrique
    du pays choisi.
    """

    def __init__(self, pays: str) -> None:
        """
        Args:
            pays: le nom du pays.

        Attributes:
            facteur_emission_co2_kwh: facteur d'émission du pays, en
                gCO2e/kWh (float).
            emissions_co2: dernier résultat calculé par convertir_co2(), en
                gCO2e (float, 0 tant qu'aucune conversion n'a été faite).

        Returns:
            None.

        """

        self.pays: str = pays
        self.facteur_emission_co2_kwh: float = FacteurEmissionPays().obtenir_facteur(pays)
        self.emissions_co2: float = 0  # valeurs

    def convertir_co2(self, energie_kwh: float) -> float:
        """Convertit une énergie en émissions de CO2.

        Formule : Émissions (gCO2e) = Énergie (kWh) x Facteur (gCO2e/kWh).

        Args:
            energie_kwh: l'énergie consommée, en kWh.

        Returns:
            float: les émissions de CO2 estimées, en gCO2e.
        """
        self.emissions_co2 = energie_kwh * self.facteur_emission_co2_kwh
        return self.emissions_co2

    def calculer_score(self) -> int:
        """Convertit les émissions mémorisées en score sur 100.

        Barème en gCO2e (à ajuster/justifier) :
            < 0.001 -> 100
            < 0.1   -> 70
            < 100   -> 30
            sinon   -> 0

        Returns:
            int: un score entre 0 et 100, où 100 signifie des émissions
            négligeables.
        """
        if self.emissions_co2 < 0.001:
            return 100
        elif self.emissions_co2 < 0.1:
            return 70
        elif self.emissions_co2 < 100:
            return 30
        else:
            return 0
