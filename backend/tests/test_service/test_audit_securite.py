from unittest.mock import Mock, patch

import pytest

from service.AuditSecurite import AuditSecurite


@pytest.fixture
def audit():
    return AuditSecurite(1)


@patch("business_object.vulnerabilite.Vulnerabilite.nb_vulnerabilites_critiques")
def test_obtenir_vulnerabilites_critiques(mock_nb,
        audit):

    mock_nb.return_value = 3

    resultat = audit.obtenir_vulnerabilites_critiques()

    assert resultat == 3

    mock_nb.assert_called_once_with(
        audit.vulnerabilites
    )


@patch("business_object.vulnerabilite.Vulnerabilite.nb_vulnerabilites_fortes")
def test_obtenir_vulnerabilites_fortes(
        mock_nb,
        audit):

    mock_nb.return_value = 2

    resultat = audit.obtenir_vulnerabilites_fortes()

    assert resultat == 2


@patch("business_object.vulnerabilite.Vulnerabilite.nb_vulnerabilites_moyennes")
def test_obtenir_vulnerabilites_moyennes(
        mock_nb,
        audit):

    mock_nb.return_value = 1

    resultat = audit.obtenir_vulnerabilites_moyennes()

    assert resultat == 1


@patch("business_object.vulnerabilite.Vulnerabilite.nb_vulnerabilites_faibles")
def test_obtenir_vulnerabilites_faibles(
        mock_nb,
        audit):

    mock_nb.return_value = 4

    resultat = audit.obtenir_vulnerabilites_faibles()

    assert resultat == 4


def test_score_vulnerabilite(audit):

    vuln1 = Mock()
    vuln1.severite.score.return_value = 4

    vuln2 = Mock()
    vuln2.severite.score.return_value = 2

    audit.vulnerabilites = [vuln1, vuln2]

    assert audit.score_vulnerabilite() == 6


def test_score_licence(audit):

    package1 = Mock()
    package1.licence.score_licence.return_value = 0

    package2 = Mock()
    package2.licence.score_licence.return_value = 3

    audit.packages = [
        package1,
        package2
    ]

    assert audit.score_licence() == 3


def test_score_total_securite(audit):

    audit.score_vulnerabilite = lambda: 8
    audit.score_licence = lambda: 3

    assert audit.score_total_securite() == 11


def test_initialisation_audit():

    audit = AuditSecurite(42)

    assert audit.id == 42

    assert audit.packages == []

    assert audit.vulnerabilites == []

    assert audit.date is not None
