class EstimateurEnergie:
    """Estime l'énergie théorique (kWh) consommée par un code, à partir de sa
    complexité algorithmique et de trois hypothèses documentées.

    """

    def __init__(
        self,
        taille_entree: int = 1000,
        temps_par_operation: float = 80e-9,  # 80 ns
        puissance_watts: float = 50,
    ) -> None:
        """Initialise l'estimateur avec ses trois hypothèses.

        Args:
            taille_entree: taille de référence n (défaut : 1000).
            temps_par_operation: secondes par opération élémentaire
                (défaut : 80 ns).
            puissance_watts: puissance de la machine type en watts
                (défaut : 50 W).

        Returns:
            None.
        """
        self.taille_entree: int = taille_entree
        self.temps_par_operation: float = temps_par_operation
        self.puissance_watts: float = puissance_watts

    def estimer_operations(self, complexite: int) -> int:
        """Estime le nombre d'opérations pour une complexité O(n^k).

        Args:
            complexite: l'exposant k de O(n^k), c'est-à-dire la
                profondeur maximale d'imbrication des boucles
                (0 -> O(1), 1 -> O(n), 2 -> O(n²), ...).

        Returns:
            int: le nombre d'opérations estimé, soit taille_entree ** k.
        """
        return self.taille_entree**complexite

    def estimer_temps(self, nb_operations: int) -> float:
        """Convertit un nombre d'opérations en temps d'exécution.

        Args:
            nb_operations: le nombre d'opérations élémentaires.

        Returns:
            float: le temps d'exécution théorique, en secondes.
        """
        return nb_operations * self.temps_par_operation

    def estimer_energie_kwh(self, temps: float) -> float:
        """Convertit un temps d'exécution en énergie consommée.

        Formule : Énergie (J) = Puissance (W) x Temps (s), puis
        conversion en kWh (1 kWh = 3 600 000 J).

        Args:
            temps: le temps d'exécution, en secondes.

        Returns:
            float: l'énergie théorique consommée, en kWh.
        """
        joules = self.puissance_watts * temps
        return joules / 3_600_000