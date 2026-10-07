"""ParsingAST : classe sans état chargée de transformer le code Python
soumis (texte brut) en arbre syntaxique abstrait (AST), exploitable par
les analyseurs du pipeline F3.
"""

import ast


class ParsingAST:
    """Transforme du code Python (str) en arbre AST."""

    def parse(self, code: str) -> ast.AST:
        """Parse le code source et retourne l'arbre AST correspondant.

        Args:
            code: le code source Python, sous forme de texte brut.

        Returns:
            L'arbre syntaxique abstrait (ast.AST) correspondant au code.

        Raises:
            SyntaxError: si le code soumis n'est pas un code Python valide.
        """
        return ast.parse(code)
