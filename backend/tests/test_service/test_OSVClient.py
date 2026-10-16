from unittest.mock import Mock, patch

import pytest
import requests

from business_object.package import Package
from service.OSVclient import OSVClient


@pytest.fixture
def package_test():

    return Package(
        nom="django",
        version="4.2.0",
        ecosysteme="PyPI",
        licence=None
    )


@patch("service.osv_client.requests.post")
def test_interroger_api_retourne_json(mock_post, package_test):
    """
    Test simule une réponse contenant une vulnérabilité et vérifie qu'elle
    est transmise sans modification.
    """

    reponse_json = {
        "vulns": [
            {
                "id": "CVE-2024-1234"
            }
        ]
    }

    mock_response = Mock()
    mock_response.json.return_value = reponse_json

    mock_post.return_value = mock_response

    client = OSVClient()

    resultat = client.interroger_api(package_test)

    assert resultat == reponse_json


@patch("service.osv_client.requests.post")
def test_interroger_api_construit_bon_payload(mock_post, package_test):
    """
    Vérifie que la méthode interroger_api construit correctement le payload envoyé à l'API OSV.
    Assure que le nom, la version et l'écosystème du package sont bien inclus dans la requête HTTP
    """
    mock_response = Mock()
    mock_response.json.return_value = {}

    mock_post.return_value = mock_response

    client = OSVClient()

    client.interroger_api(package_test)

    mock_post.assert_called_once_with(
        OSVClient.URL_API_OSV,
        json={
            "version": "4.2.0",
            "package": {
                "name": "django",
                "ecosystem": "PyPI"
            }
        },
        timeout=10
    )


@patch("service.osv_client.requests.post")
def test_raise_for_status_est_appele(mock_post, package_test):
    """
    Teste si la méthode raise_for_status est appelée après la réception de la réponse HTTP.
    """

    mock_response = Mock()

    mock_response.json.return_value = {}

    mock_post.return_value = mock_response

    client = OSVClient()

    client.interroger_api(package_test)

    mock_response.raise_for_status.assert_called_once()


@patch("service.osv_client.requests.post")
def test_interroger_api_erreur_http(mock_post, package_test):
    """
    Teste si les erreurs HTTP sont bien levées par la méthode interroger_api.
    """
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError()
    )

    mock_post.return_value = mock_response

    client = OSVClient()

    with pytest.raises(
            requests.exceptions.HTTPError):

        client.interroger_api(package_test)


@patch("service.osv_client.requests.post")
def test_interroger_api_reponse_vide(mock_post, package_test):
    """
    Teste si la méthode interroger_api renvoie bien un dictionnaire vide
    si lle reçoit une réponse vide de l'API OSV.

    """
    mock_response = Mock()

    mock_response.json.return_value = {}

    mock_post.return_value = mock_response

    client = OSVClient()

    resultat = client.interroger_api(package_test)

    assert resultat == {}
