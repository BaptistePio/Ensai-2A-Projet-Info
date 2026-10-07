import ast


class AnalyseurBoucle(ast.NodeVisitor):
    """Détecte les boucles imbriquées for et while (anti-pattern énergivore)
    dans l'AST en s'appuyant sur le mécanisme de parcours fourni par ast.NodeVisitor.

    Hérite de NodeVisitor (module ast) pour réutiliser son mécanisme de
    parcours automatique de l'arbre (visit() / generic_visit()). Seules
    les méthodes visit_For et visit_While sont redéfinies ici : leur nom
    est imposé par NodeVisitor, qui les appelle automatiquement dès qu'il
    rencontre un nœud du type correspondant.
    """

    def __init__(self):
        self.imbrication_actuelle: int = 0
        self.imbrication_max: int = 0
        self.boucles_imbriquees: list[int] = []  # Numéros de ligne ou il y a des boucles imbriquees

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
            None. Met à jour imbrication_actuelle, imbrication_max et
            boucles_imbriquees.

        """
        self.imbrication_actuelle += 1  # Entrée dans une boucle
        self.imbrication_max = max(self.imbrication_max, self.imbrication_actuelle)
        # Met à jour la profondeur max atteinte

        if self.imbrication_actuelle >= 2:  # Si on est dans une boucle imbriquée
            self.boucles_imbriquees.append(noeud.lineno)  # On enregistre le numéro de la ligne
            # dans la liste boucles_imbriquees

        self.generic_visit(noeud)  # On continue à explorer l'intérieur de la boucle
        self.imbrication_actuelle -= 1  # On sort de la boucle

    def calculer_score(self) -> int:
        """Convertit l'imbrication maximale détectée en un score sur 100.

        Barème (à ajuster/justifier selon nos hypothèses) :
            0 boucle imbriquée  -> 100
            1 niveau d'imbrication -> 80
            2 niveaux -> 40
            3 niveaux ou plus -> 0

        Args:
            Aucun (lit directement self.imbrication_max).

        Returns:
            int: un score entre 0 et 100, où 100 signifie aucune boucle
            imbriquée détectée, et 0 une imbrication sévère (3 niveaux
            ou plus).
        """
        if self.imbrication_max == 0:
            return 100
        elif self.imbrication_max == 1:
            return 80
        elif self.imbrication_max == 2:
            return 40
        else:
            return 0
