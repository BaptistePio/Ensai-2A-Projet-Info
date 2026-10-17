import pytest

from business_object.risque import Risque
from business_object.severite import Severite
from business_object.vulnerabilite import Vulnerabilite


def test_nb_vulnerabilites_critiques(liste_vulnerabilites):

    assert Vulnerabilite.nb_vulnerabilites_critiques(liste_vulnerabilites) == 1


def test_nb_vulnerabilites_fortes(liste_vulnerabilites):

    assert Vulnerabilite.nb_vulnerabilites_fortes(liste_vulnerabilites) == 1


def test_nb_vulnerabilites_moyennes(liste_vulnerabilites):

    assert Vulnerabilite.nb_vulnerabilites_moyennes(liste_vulnerabilites) == 1


def test_nb_vulnerabilites_faibles(liste_vulnerabilites):

    assert Vulnerabilite.nb_vulnerabilites_faibles(liste_vulnerabilites) == 1


def test_id_vulnerabilite(vulnerabilite_high):
    assert vulnerabilite_high.id == "GHSA-1234"


def test_description_vulnerabilite(vulnerabilite_high):
    assert vulnerabilite_high.description == "Vulnérabilité de test"


def test_version_corrigee(vulnerabilite_high):
    assert vulnerabilite_high.version_corrigee == "4.2.1"


def test_severite_vulnerabilite(vulnerabilite_high):
    assert vulnerabilite_high.severite.niveau_severite == "HIGH"


def test_packages_vulnerabilite(vulnerabilite_high):
    assert len(vulnerabilite_high.packages) == 1
    assert vulnerabilite_high.packages[0].nom == "django"


# on utilise des fixtures si l'objet est complexe a construire: Package, Licence Vulnerabilite
# et AuditSecurite ici. Si bcp de paramètres, utilisé dans pls tests
# mettre les fixture dans un fichier pytest
