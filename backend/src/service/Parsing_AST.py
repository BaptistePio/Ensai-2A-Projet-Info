import ast


class ParsingAST:
    """classe sans état chargée de transformer le code Python
    soumis (str) en arbre syntaxique abstrait (AST)."""

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
