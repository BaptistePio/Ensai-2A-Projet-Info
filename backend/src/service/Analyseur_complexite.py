import ast


class AnalyseurComplexite(ast.NodeVisitor):
    """Estime la complexité algorithmique du code via la profondeur
    d'imbrication des boucles for/while.
    """

    def __init__(self):
        self.profondeur_actuelle: int = 0
        self.profondeur_max: int = 0

    def visit_For(self, noeud: ast.AST) -> None:
        """Appelée automatiquement par NodeVisitor sur chaque nœud For.

        Args:
            noeud: le nœud AST de type ast.For rencontré pendant le parcours.

        Returns:
            None. Modifie l'état interne de l'objet et
            poursuit le parcours via generic_visit.
        """

        self._visiter_boucle(noeud)

    def visit_While(self, noeud: ast.AST) -> None:
        """Appelée automatiquement par NodeVisitor sur chaque nœud While.

        Args:
            noeud: le nœud AST de type ast.While rencontré pendant le parcours.

        Returns:
            None. Modifie l'état interne de l'objet et
            poursuit le parcours via generic_visit.
        """
        self._visiter_boucle(noeud)

    def _visiter_boucle(self, noeud: ast.AST) -> None:
        """Logique commune à visit_For et visit_While.

        Incrémente la profondeur à l'entrée de la boucle, continue le
        parcours à l'intérieur via generic_visit (indispensable pour
        détecter une boucle imbriquée à l'intérieur de celle-ci), puis
        décrémente la profondeur à la sortie.

        Args:
            noeud: le nœud AST (ast.For ou ast.While) actuellement visité.

        Returns:
            None. Met à jour profondeur_actuelle, profondeur_max

        """
        self.profondeur_actuelle += 1
        self.profondeur_max = max(self.profondeur_max, self.profondeur_actuelle)
        # Met à jour la profondeur max atteinte

        self.generic_visit(noeud)

        self.profondeur_actuelle -= 1

    def complexite(self) -> str:
        """Traduit profondeur_max en notation Big-O.

        0 boucle -> O(1)
        1 niveau -> O(n)
        2 niveaux -> O(n²)
        3 niveaux -> O(n³)
        n niveaux -> O(n^k), généralisation

        Args:
            Aucun (lit directement self.profondeur_max).

        Returns:
            str: la notation Big-O correspondante.

        """
        mapping = {0: "O(1)", 1: "O(n)", 2: "O(n²)", 3: "O(n³)"}  # Créer un dict Python
        if self.profondeur_max in mapping:  # Vérifie si la valeur de profondeur_max existe comme
            # clé dans le dict
            return mapping[self.profondeur_max]
        return f"O(n^{self.profondeur_max})"  # Si la condition du if est fausse

    def calculer_score(self) -> int:
        """Convertit la complexité estimée en score sur 100.
        Args:
            Aucun

        Returns:
            int: un score entre 0 et 100
        """
        bareme = {"O(1)": 100, "O(n)": 80, "O(n²)": 40, "O(n³)": 10}  # Créer un dict
        return bareme.get(self.complexite(), 0)
        # Le 0 est une valeur pas défaut si la compléxité n'existe pas comme clé dans le dict
