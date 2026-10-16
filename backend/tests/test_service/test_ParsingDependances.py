import pytest

from service.ParsingDependances import ParsingDependances


@pytest.fixture
def vuln_critique_json():
    return {
        "id": "CVE-2024-1234",
        "summary": "Faille critique",
        "severity": [
            {
                "score": "CVSS_V3:3.1/9.8"
            }
        ],
        "affected": [
            {
                "ranges": [
                    {
                        "events": [
                            {"fixed": "2.1.0"}
                        ]
                    }
                ]
            }
        ]
    }


def test_parser_une_vulnerabilite():
    """
    Vérifie que la méthode parser transforme correctement
    une vulnérabilité renvoyée par l'API OSV en objet métier
    Vulnerabilite.
    """
    reponse_json = {
        "vulns": [
            {
                "id": "CVE-2024-1234",
                "summary": "Faille critique",
                "severity": [
                    {
                        "score": "CVSS_V3:3.1/9.8"
                    }
                ],
                "affected": [
                    {
                        "ranges": [
                            {
                                "events": [
                                    {"fixed": "3.0.0"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    resultats = ParsingDependances.parser(reponse_json)

    assert len(resultats) == 1

    vuln = resultats[0]

    assert vuln.id_CVE == "CVE-2024-1234"
    assert vuln.description == "Faille critique"
    assert vuln.version_corrigee == "3.0.0"
    assert vuln.severite.niveau_severite == "CRITICAL"


def test_parser_plusieurs_vulnerabilites():
    """
    Vérifie que la méthode parser traite correctement
    plusieurs vulnérabilités présentes dans la réponse JSON.
    """
    reponse_json = {
        "vulns": [
            {"id": "CVE-1"},
            {"id": "CVE-2"}
        ]
    }

    resultats = ParsingDependances.parser(reponse_json)

    assert len(resultats) == 2


def test_extraire_severite_critical(vuln_critique_json):
    """
    Teste si le score CVSS est correctement converti en sévérité CRITICAL
    si il est supérieur ou égal à [seuil critique].
    """
    severite = ParsingDependances.extraire_severite(
        vuln_critique_json
    )

    assert severite.niveau_severite == "CRITICAL"


def test_extraire_severite_high():
    """
    Teste si le score CVSS est correctement converti en sévérité CRITICAL
    si il est supérieur ou égal à [seuil haut].
    """
    vuln_json = {
        "severity": [
            {
                "score": "CVSS_V3:3.1/8.0"
            }
        ]
    }

    severite = ParsingDependances.extraire_severite(vuln_json)

    assert severite.niveau_severite == "HIGH"


def test_extraire_severite_medium():
    """
    Teste si le score CVSS est correctement converti en sévérité CRITICAL
    si il est supérieur ou égal à [seuil moyen].
    """
    vuln_json = {
        "severity": [
            {
                "score": "CVSS_V3:3.1/5.4"
            }
        ]
    }

    severite = ParsingDependances.extraire_severite(vuln_json)

    assert severite.niveau_severite == "MEDIUM"


def test_extraire_severite_low():
    """
    Teste si le score CVSS est correctement converti en sévérité CRITICAL
    si il est supérieur ou égal à [seuil bas].
    """
    vuln_json = {
        "severity": [
            {
                "score": "CVSS_V3:3.1/3.2"
            }
        ]
    }

    severite = ParsingDependances.extraire_severite(vuln_json)

    assert severite.niveau_severite == "LOW"


def test_extraire_severite_aucune_severite():
    """
    Test si la sévérité renvoyée est bien "LOW" lorsqu'aucune information 
    de sévérité n'est fournie par l'API OSV.
    """
    vuln_json = {}

    severite = ParsingDependances.extraire_severite(vuln_json)

    assert severite.niveau_severite == "LOW"


def test_version_corrigee():
    """
    Test si version corrigee extraite par la méthode version_corrigee() est correcte
    """
    vuln_json = {
        "affected": [
            {
                "ranges": [
                    {
                        "events": [
                            {"introduced": "1.0"},
                            {"fixed": "2.3.0"}
                        ]
                    }
                ]
            }
        ]
    }

    version = ParsingDependances.version_corrigee(vuln_json)

    assert version == "2.3.0"


def test_version_corrigee_absente():

    vuln_json = {
        "affected": []
    }

    version = ParsingDependances.version_corrigee(vuln_json)

    assert version is None


def test_parser_une_vulnerabilite():
    """
    Permet de parser le fichier dans le cas où il n'y a qu'une seule vulnérabilité
    """

    reponse_json = {
        "vulns": [
            {
                "id": "CVE-2024-1234",
                "summary": "Faille critique",
                "severity": [
                    {
                        "score": "CVSS_V3:3.1/9.8"
                    }
                ],
                "affected": [
                    {
                        "ranges": [
                            {
                                "events": [
                                    {"fixed": "3.0.0"}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    resultats = ParsingDependances.parser(reponse_json)

    assert len(resultats) == 1

    vuln = resultats[0]

    assert vuln.id_CVE == "CVE-2024-1234"
    assert vuln.description == "Faille critique"
    assert vuln.version_corrigee == "3.0.0"
    assert vuln.severite.niveau_severite == "CRITICAL"


def test_parser_plusieurs_vulnerabilites():
    """
    Permet de parser les fichiers de dépendances dans le cas où il y a plusieurs dépendances
    """

    reponse_json = {
        "vulns": [
            {"id": "CVE-1"},
            {"id": "CVE-2"}
        ]
    }

    resultats = ParsingDependances.parser(reponse_json)

    assert len(resultats) == 2


def test_parser_aucune_vulnerabilite():
    """
    Cas où le fichier ne présente aucune vulnérabilités
    """

    reponse_json = {}

    resultats = ParsingDependances.parser(reponse_json)

    assert resultats == []


def test_parser_severite_par_defaut():
    """
    Test d'un cas particulier: si le fichier et sa vulnérabilité n'indique pas de sévérité
    """

    reponse_json = {
        "vulns": [
            {
                "id": "CVE-2024-1111",
                "summary": "test"
            }
        ]
    }

    resultats = ParsingDependances.parser(reponse_json)

    vuln = resultats[0]

    assert vuln.severite.niveau_severite == "LOW"
