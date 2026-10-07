"""AnalyseurRecursion : détecte les fonctions qui s'appellent elles-mêmes
(récursion directe uniquement), via ast.NodeVisitor.
"""

import ast


class AnalyseurRecursion(ast.NodeVisitor):
    """Détecte la récursion directe (une fonction qui s'appelle elle-même).

    Limite : seule la récursion DIRECTE est détectée. La récursion
    indirecte n'est pas détectée, car cela nécessiterait de
    suivre les appels à travers plusieurs fonctions.
    """

    def __init__(self):
        self.fonction_actuelle: str | None = None
        self.fonctions_recursives: list[str] = []

    def visit_FunctionDef(self, node: ast.AST) -> None:
        """Appelée à chaque définition de fonction rencontrée.

        Mémorise le nom de la fonction dont on explore le corps, puis
        continue le parcours à l'intérieur via generic_visit. On restaure
        la fonction précédente en sortant, pour gérer correctement les
        fonctions imbriquées (une fonction définie dans une autre).
        """
        fonction_precedente = self.fonction_actuelle
        self.fonction_actuelle = node.name

        self.generic_visit(node)  # explore le corps de la fonction

        self.fonction_actuelle = fonction_precedente

    def visit_Call(self, node: ast.AST) -> None:
        """Appelée à chaque appel de fonction rencontré.

        Si le nom de la fonction appelée correspond à la fonction
        actuellement explorée, c'est de la récursion directe.
        """
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == self.fonction_actuelle
            and self.fonction_actuelle not in self.fonctions_recursives
        ):
            self.fonctions_recursives.append(self.fonction_actuelle)

        self.generic_visit(node)

    def calculer_score(self) -> int:
        """Convertit le nombre de fonctions récursives détectées en score.

        Barème (à ajuster/justifier) :
            0 fonction récursive -> 100
            1 fonction récursive -> 50
            2 et + -> 0
        """
        nb_fonctions = len(self.fonctions_recursives)
        if nb_fonctions == 0:
            return 100
        elif nb_fonctions == 1:
            return 50
        else:
            return 0
