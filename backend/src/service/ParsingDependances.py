from risque import Risque
from severite import Severite
from vulnerabilite import Vulnerabilite


class ParsingDependances:
    @staticmethod
    def parser(reponse_json):
        """
        Transforme la réponse rnvoyée par l'API OSV au format json en une liste de vulnérabilités
        Cette transformation permettra de traiter les données pour l'audit de sécurité.
        """

        vulnerabilites = []

        for vulnerabilite_json in reponse_json.get("vulns", []):
            id_cve = vulnerabilite_json.get("id")

            description = vulnerabilite_json.get("summary", "non rensignée")
            # vulnerabilite_json est un dico
            # si la clé summary n'est pas présente (pas de description dans la BDD)
            # alors "non renseignée": fonctionne comme un if/else

            severite = ParsingDependances.extraire_severite(vulnerabilite_json)

            version_corrigee = ParsingDependances.version_corrigee(vulnerabilite_json)

            vuln = Vulnerabilite(
                id_CVE=id_cve,
                packages=[],
                description=description,
                severite=severite,
                version_corrigee=version_corrigee,
            )

            vulnerabilites.append(vuln)

        return vulnerabilites


@staticmethod
def extraire_severite(vulnerabilite_json):

    severity_list = vulnerabilite_json.get("severity", [])

    if not severity_list:
        return Severite("LOW")

    score_cvss = float(
        severity_list[0]["score"]
        .split("/")[-1]
    )

    if score_cvss >= 9:
        return Severite("CRITICAL")

    if score_cvss >= 7:
        return Severite("HIGH")

    if score_cvss >= 4:
        return Severite("MEDIUM")

    return Severite("LOW")


@staticmethod
def version_corrigee(vulnerabilite_json):

    affected = vulnerabilite_json.get("affected", [])

    for item in affected:

        for r in item.get("ranges", []):

            for event in r.get("events", []):

                if "fixed" in event:
                    return event["fixed"]

    return None
