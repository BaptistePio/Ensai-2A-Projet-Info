from unittest.mock import Mock, patch

import pytest
import requests

from business_object.package import Package
from service.OSVservice import OSVService


@pytest.fixture
def package_test():
    return Package(
        nom="django",
        version="4.2",
        ecosysteme="PyPI",
        licence=None
    )


def test_scanner_appelle_osvclient(package_test):
    """
    test si la methode statique scanner fait bien appelle à OSVClient
    """

    client_mock = Mock()

    client_mock.interroger_API.return_value = {}

    service = OSVService(client_mock)

    service.scanner(package_test)

    client_mock.interroger_API.assert_called_once_with(
        package_test
    )


@patch("service.OSVservice.ParsingDependances.parser")
def test_scanner_appelle_parser(mock_parser, package_test):
    """
    Teste si la méthode scanner() appelle bien la méthode statique 
    parser() de ParsingDpendances
    """
    client_mock = Mock()

    reponse_json = {
        "vulns": []
    }

    client_mock.interroger_API.return_value = reponse_json

    service = OSVService(client_mock)

    service.scanner(package_test)

    mock_parser.assert_called_once_with(
        reponse_json
    )


@patch("service.OSVservice.ParsingDependances.parser")
def test_scanner_retourne_vulnerabilites(mock_parser, package_test):
    """
    teste si la méthode scanner() renvoie bien la liste des vulnérabilités
    produite par ParsingDependances.parser().
    """
    client_mock = Mock()

    client_mock.interroger_API.return_value = {
        "vulns": []
    }

    liste_vulns = ["v1", "v2"]

    mock_parser.return_value = liste_vulns

    service = OSVService(client_mock)

    resultat = service.scanner(package_test)

    assert resultat == liste_vulns


@patch("service.OSVservice.ParsingDependances.parser")
def test_scanner_aucune_vulnerabilite(mock_parser, package_test):
    """
    Vérifie que la méthode scanner renvoie bien une liste vide dans le cas
    pù il n'a aucune vulnérabilité.
    """
    client_mock = Mock()

    client_mock.interroger_API.return_value = {}

    mock_parser.return_value = []

    service = OSVService(client_mock)

    resultat = service.scanner(package_test)

    assert resultat == []


url = "https://api.osv.dev/v1/query"

payload = {
    "version": "2.25.1",
    "package": {
        "name": "requests",
        "ecosystem": "PyPI"
    }
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())