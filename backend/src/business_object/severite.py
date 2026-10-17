class Severite:

    MAPPING_severite = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
        }

    def __init__(self, niveau_severite: str):
        self.niveau_severite = niveau_severite

    def score_severite(self):
        """
        Renvoie le score associé à la sévérité dans le mapping de référence
        """
        return self.MAPPING_severite.get(self.niveau_severite, 0)

    def __repr__(self):
        return (
            f"Severite(niveau_severite='{self.niveau_severite}',"f"score_severite= {self.score_severite()})"
        )


s = Severite("LOW")
print(s)