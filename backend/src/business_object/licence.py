from business_object.licence_risque import LicenceRisque


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

    def __repr__(self):
        return (
            f"Licence(idspdx='{self.idspdx}', "
            f"nom='{self.nom}', "
            f"opensource={self.opensource}, "
            f"score_licence = {self.score_licence()})"
        )


licence = Licence(
    idspdx="GPL-3.0",
    nom="GNU General Public License v3.0",
    opensource=True
)

print(licence)

# cas où la licence ne se trouve pas dans le mapping.
licence2 = Licence(
    idspdx="MA-LICENCE",
    nom="Ma licence",
    opensource=True
)

print(licence2)