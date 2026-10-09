

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
        """
        returns
        -------
        int
            Renvoie le score du risque associé au package.
        """

        return self.SCORES_RISQUE.get(self.niveau_risque,0) 
##le .get permet de renvoyer none plutot qu'une erreur si la clé n'existe pas

#Dans Audit Securité 
#score_total = (vulnerabilite.risque.score_risque() + vulnerabilite.severite.score()+ licence.score_licence())