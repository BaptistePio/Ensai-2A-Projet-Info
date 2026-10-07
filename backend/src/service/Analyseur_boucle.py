"""AnalyseurBoucle : détecte les boucles imbriquées (for/while) dans l'AST,
en s'appuyant sur le mécanisme de parcours fourni par ast.NodeVisitor.
"""

import ast


class AnalyseurBoucle(ast.NodeVisitor):
    """Détecte les boucles imbriquées (anti-pattern énergivore).

    Hérite de NodeVisitor (module ast) pour réutiliser son mécanisme de
    parcours automatique de l'arbre (visit() / generic_visit()). Seules
    les méthodes visit_For et visit_While sont redéfinies ici : leur nom
    est imposé par NodeVisitor, qui les appelle automatiquement dès qu'il
    rencontre un nœud du type correspondant.
    """

    def __init__(self):
        self.imbrication_actuelle: int = 0
        self.imbrication_max: int = 0
        self.boucles_imbriquees: list[int] = []  # numéros de ligne

    def visit_For(self, node: ast.AST) -> None:
        self._visiter_boucle(node)

    def visit_While(self, node: ast.AST) -> None:
        self._visiter_boucle(node)

    def _visiter_boucle(self, node: ast.AST) -> None:
        """Logique commune à visit_For et visit_While.

        Incrémente la profondeur à l'entrée de la boucle, continue le
        parcours à l'intérieur via generic_visit (indispensable pour
        détecter une boucle imbriquée à l'intérieur de celle-ci), puis
        décrémente la profondeur à la sortie.
        """
        self.imbrication_actuelle += 1
        self.imbrication_max = max(self.imbrication_max, self.imbrication_actuelle)

        if self.imbrication_actuelle >= 2:
            self.boucles_imbriquees.append(node.lineno)

        self.generic_visit(node)  # continue à explorer l'intérieur de la boucle
        self.imbrication_actuelle -= 1

    def calculer_score(self) -> int:
        """Convertit l'imbrication maximale détectée en un score sur 100.

        Barème (à ajuster/justifier selon nos hypothèses) :
            0 boucle imbriquée  -> 100
            1 niveau d'imbrication -> 80
            2 niveaux -> 40
            3 niveaux ou plus -> 0
        """
        if self.imbrication_max == 0:
            return 100
        elif self.imbrication_max == 1:
            return 80
        elif self.imbrication_max == 2:
            return 40
        else:
            return 0
