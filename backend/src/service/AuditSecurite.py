
from datetime import datetime

from package import Package
from vulnerabilite import Vulnerabilite


class AuditSecurite:
    """
    Réalise un audit de sécurité concernant les vulnérabilités des packages et les risques des licences utilisées
    """

    def __init__(self, id_audit):
        self.id = id_audit
        self.date = datetime.now()

        self.packages = []
        self.vulnerabilites = []

    def obtenir_vulnerabilites_critiques(self):
        """ Permet d'obtenir les vulnérabilités catégorisées critiques par le mapping.
        Return
        ------
        Renvoie les vulnérabilités critiques.

        """
        return Vulnerabilite.nb_vulnerabilites_critiques(
            self.vulnerabilites
        )

    def obtenir_vulnerabilites_fortes(self):
        """ Permet d'obtenir les vulnérabilités catégorisées fortes par le mapping.
        Return
        ------
        Vulnerabilite
            Renvoie les vulnérabilités fortes.

        """
        return Vulnerabilite.nb_vulnerabilites_fortes(
            self.vulnerabilites
        )

    def obtenir_vulnerabilites_moyennes(self):
        """ Permet d'obtenir les vulnérabilités catégorisées moyennes par le mapping.
        Return
        ------
        Vulnerabilite
            Renvoie les vulnérabilités moyennes.

        """
        return Vulnerabilite.nb_vulnerabilites_moyennes(
            self.vulnerabilites
        )

    def obtenir_vulnerabilites_faibles(self):
        """ Permet d'obtenir les vulnérabilités catégorisées faibles par le mapping.
        Return
        ------
        Vulnerabilite
            Renvoie les vulnérabilités faibles.

        """
        return Vulnerabilite.nb_vulnerabilites_faibles(
            self.vulnerabilites
        )

    def score_vulnerabilite(self):
        """ Permet d'obtenir le score attribué quand aux vulnerérabilités.
        Return
        ------
        int
            Renvoie le score pour une vulnérabilité.

        """

        return sum(
            v.risque.score_risque()
            + v.severite.score()
            for v in self.vulnerabilites
        )

    def score_licence(self):
        """ Permet d'obtenir le score attribué quand aux licences.
        Return
        ------
        int
            Renvoie le score pour une lience.

        """
        return sum(
            p.licence.score_licence()
            for p in self.packages
        )

    def score_total_securite(self):
        """ Permet d'obtenir un score total pour la sécurité par aggrégation des deux scores.
        Return
        ------
        int
            Renvoie la somme des scores pour une vulnérabilité et pour un risque.

        """
        return (
            self.score_vulnerabilite()
            + self.score_licence()
        )

#on a 2 packages: Numpy de risque 0 et et Django de risque 3
#score_licence renvoie 3

#V1 :risque = HIGH -> 3 et severite = CRITICAL -> 4
#V2 : risque = LOW -> 1 et severite = MEDIUM -> 2
#alors score_vulnerabilites renvoie (3+4) + (1+2)


#score total vulnerabilite renvoie 13