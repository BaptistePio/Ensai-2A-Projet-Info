import ast


class AnalyseurComplexite(ast.NodeVisitor):
    """Estime la complexité algorithmique du code via la profondeur
    d'imbrication des boucles for/while.
    """

    def __init__(self):
        self.profondeur_actuelle: int = 0
        self.profondeur_max: int = 0

    def visit_For(self, node: ast.AST) -> None:
        self._visiter_boucle(node)

    def visit_While(self, node: ast.AST) -> None:
        self._visiter_boucle(node)

    def _visiter_boucle(self, node: ast.AST) -> None:
        self.profondeur_actuelle += 1
        self.profondeur_max = max(self.profondeur_max, self.profondeur_actuelle)

        self.generic_visit(node)

        self.profondeur_actuelle -= 1

    def complexite(self) -> str:
        """Traduit profondeur_max en notation Big-O.
 
        0 boucle -> O(1)
        1 niveau -> O(n)
        2 niveaux -> O(n²)
        3 niveaux -> O(n³)
        n niveaux -> O(n^k), généralisation
        """
        mapping = {0: "O(1)", 1: "O(n)", 2: "O(n²)", 3: "O(n³)"}
        if self.profondeur_max in mapping:
            return mapping[self.profondeur_max]
        return f"O(n^{self.profondeur_max})"

    def calculer_score(self) -> int:
        """Convertit la complexité estimée en score sur 100."""
        bareme = {"O(1)": 100, "O(n)": 80, "O(n²)": 40, "O(n³)": 10}
        return bareme.get(self.complexite(), 0)
