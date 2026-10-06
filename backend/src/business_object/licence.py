from licence_risque import LicenceRisque


class Licence:

    def __init__(self, id, nom, opensource: bool):
        self.idspdx = idspdx
        self.nom = nom
        self.opensource = opensource

    def score_licence(self):
        return LicenceRisque.obtenir_score(self)
