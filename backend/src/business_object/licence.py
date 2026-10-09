from licence_risque import LicenceRisque


class Licence:

    def __init__(self, idspdx, nom, opensource: bool):
        self.idspdx = idspdx
        self.nom = nom
        self.opensource = opensource

    def score_licence(self):
        """ interroge l'API OSV grace à une requête HTML et retourne sa réponse au format json

        Return
        ------
        Renvoie le score de la licence à risque considérée.
"""
        return LicenceRisque.obtenir_score(self)
