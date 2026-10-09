class Severite:

    MAPPING_severite = {
        "CRITICAL": 4,
        "HIGH": 3,
        "MEDIUM": 2,
        "LOW": 1
        }

    def __init__(self, niveau_severite):
        self.niveau_severite = niveau_severite

    def score(self):
        return self.MAPPING_severite[self.niveau_severite]