from .package import Package
from .severite import Severite


class Vulnerabilite:
    def __init__(
        self,
        id_CVE: int, 
        packages: list[Package],
        description,
        severite: Severite,
        version_corrigee
        ):

        self.id_CVE = id_CVE
        self.packages = packages
        self.description = description
        self.severite = severite
        self.version_corrigee = version_corrigee

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
        return sum(v.severite.score_severite() for v in self.vulnerabilites)

    def __repr__(self):
        return (
            f"Vulnerabilite("
            f"id='{self.id_CVE}', "
            f"packages={self.packages},"
            f"description='{self.description}',"
            f"severite={self.severite})"
        )


v = Vulnerabilite(
    "GHSA-123",
    ["django", "requests"],
    "Exemple de vulnérabilité",
    Severite("HIGH"),
    "1.2.3"
)

print(v)