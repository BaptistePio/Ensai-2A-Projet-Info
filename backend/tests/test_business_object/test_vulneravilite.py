import pytest
from risque import Risque
from severite import Severite
from vulnerabilite import Vulnerabilite

#on utilise des fixtures si l'objet est complexe a construire: Package, Licence Vulnerabilite
#  et AuditSecurite ici. Si bcp de paramètres, utilisé dans pls tests
#mettre les fixture dans un fichier pytest

@pytest.fixture
def liste_vulnerabilites():

    return [
        Vulnerabilite(
            "CVE-1",
            [],
            "desc",
            Risque("HIGH"),
            Severite("CRITICAL"),
            "1.0"
        ),

        Vulnerabilite(
            "CVE-2",
            [],
            "desc",
            Risque("HIGH"),
            Severite("HIGH"),
            "1.0"
        ),

        Vulnerabilite(
            "CVE-3",
            [],
            "desc",
            Risque("LOW"),
            Severite("MEDIUM"),
            "1.0"
        ),

        Vulnerabilite(
            "CVE-4",
            [],
            "desc",
            Risque("LOW"),
            Severite("LOW"),
            "1.0"
        )
    ]


def test_nb_vulnerabilites_critiques(liste_vulnerabilites):

    assert (
        Vulnerabilite.nb_vulnerabilites_critiques(liste_vulnerabilites) == 1
    )


def test_nb_vulnerabilites_fortes(liste_vulnerabilites):

    assert (
        Vulnerabilite.nb_vulnerabilites_fortes(liste_vulnerabilites) == 1
    )


def test_nb_vulnerabilites_moyennes(liste_vulnerabilites):

    assert (
        Vulnerabilite.nb_vulnerabilites_moyennes(liste_vulnerabilites) == 1
    )


def test_nb_vulnerabilites_faibles(liste_vulnerabilites):

    assert (
        Vulnerabilite.nb_vulnerabilites_faibles(liste_vulnerabilites) == 1
    )
