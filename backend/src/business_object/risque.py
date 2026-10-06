

class Risque:
    """
    """
    SCORES_RISQUE = {
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
        }

    def __init__(self, niveau_risque: str):
        self.niveau_risque = niveau_risque

    def score_risque(self):
        return self.SCORES_risque[self.niveau_risque]

