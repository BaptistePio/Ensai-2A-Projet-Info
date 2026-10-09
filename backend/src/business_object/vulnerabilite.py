from package import Package
from risque import Risque
from severite import Severite


class Vulnerabilite:
    def __init__(self, id_CVE, packages: list[Package], description, risque: Risque, severite: Severite, version_corrigee):
        self.id_CVE = id_CVE
        self.packages = packages
        self.description = description
        self.risque = risque
        self.version_corrigee = version_corrigee
        self.severite = severite

    @staticmethod
    def nb_vulnerabilites_critiques(vulnerabilites):
        return sum(1 for v in vulnerabilites if v.severite.niveau_severite.upper() == "CRITICAL")

    @staticmethod
    def nb_vulnerabilites_fortes(vulnerabilites):
        return sum(1 for v in vulnerabilites if v.severite.niveau_severite.upper() == "HIGH")

    @staticmethod
    def nb_vulnerabilites_faibles(vulnerabilites):
        return sum(1 for v in vulnerabilites if v.severite.niveau_severite.upper() == "LOW")

    @staticmethod
    def nb_vulnerabilites_moyennes(vulnerabilites):
        return sum(1 for v in vulnerabilites if v.severite.niveau_severite.upper() == "MEDIUM")

    def score_vulnerabilites(self):
        return sum(v.risque.score_risque()+ v.severite.score_severite() for v in self.vulnerabilites)