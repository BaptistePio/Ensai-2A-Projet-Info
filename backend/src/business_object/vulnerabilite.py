from severite import Severite
from risque import Risque
from Package import Package

class Vulnerabilite:
    def __init__(self, id_CVE, packages, description, risque, severite, version_corrigée):
        self.id_CVE = id_CVE
        self.packages = []
        self.description = description
        self.risque = risque
        self.severite = serverite

    @staticmethod
    def nb_vulnerabilites_critiques(vulnerabilites):

        return sum(1
        for v in vulnerabilites
        if v.severite.niveau_severite == "CRITICAL"
            )

    def nb_vulnerabilites_fortes(vulnerabilites):
        return sum(1 for v in vulnerabilites
        if v.severite.niveau_severite == "HIGH")

    def nb_vulnerabilites_faibles(vulnerabilites):
        return sum(1 for v in vulnerabilites
        if v.severite.niveau_severite == "LOW")

    def nb_vulnerabilites_moyennes():
        return sum(1 for v in vulnerabilities
        if v.severite.niveau_severite == "MEDIUM")