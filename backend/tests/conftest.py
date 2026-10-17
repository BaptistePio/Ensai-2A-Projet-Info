from utils.env_variables import load_environment_variables

load_environment_variables()


# tests/conftest.py

import pytest

from business_object.licence import Licence
from business_object.package import Package
from business_object.risque import Risque
from business_object.severite import Severite
from business_object.vulnerabilite import Vulnerabilite


# -------- LICENCES --------

@pytest.fixture
def licence_mit():
    return Licence(
        idspdx="MIT",
        nom="MIT License",
        opensource=True
    )


@pytest.fixture
def licence_gpl3():
    return Licence(
        idspdx="GPL-3.0",
        nom="GNU GPL v3",
        opensource=True
    )


# -------- RISQUES --------

@pytest.fixture
def risque_faible():
    return Risque("LOW")


@pytest.fixture
def risque_moyen():
    return Risque("MEDIUM")


@pytest.fixture
def risque_eleve():
    return Risque("HIGH")


# -------- SEVERITES --------

@pytest.fixture
def severite_low():
    return Severite("LOW")


@pytest.fixture
def severite_medium():
    return Severite("MEDIUM")


@pytest.fixture
def severite_high():
    return Severite("HIGH")


@pytest.fixture
def severite_critical():
    return Severite("CRITICAL")


# -------- PACKAGES --------

@pytest.fixture
def package_requests(licence_apache):
    return Package(
        nom="requests",
        version="2.31.0",
        ecosysteme="PyPI",
        licence=licence_apache
    )


@pytest.fixture
def package_django(licence_mit):
    return Package(
        nom="django",
        version="4.2.0",
        ecosysteme="PyPI",
        licence=licence_mit
    )


@pytest.fixture
def licence_apache():
    return Licence(
        idspdx="Apache-2.0",
        nom="Apache License 2.0",
        opensource=True
    )


# -------- VULNERABILITES --------

@pytest.fixture
def vulnerabilite_high(package_django, severite_high):
    return Vulnerabilite(
        id="GHSA-1234",
        description="Vulnérabilité de test",
        severite=severite_high,
        version_corrigee="4.2.1",
        packages=[package_django]
    )


@pytest.fixture
def vulnerabilite_critical(
        package_requests,
        severite_critical):
    return Vulnerabilite(
        id="GHSA-9999",
        description="Vulnérabilité critique",
        severite=severite_critical,
        version_corrigee="2.32.0",
        packages=[package_requests]
    )

@pytest.fixture
def liste_vulnerabilites():

    return [
        Vulnerabilite("CVE-1", [], "desc", Risque("HIGH"), Severite("CRITICAL"), "1.0"),
        Vulnerabilite("CVE-2", [], "desc", Risque("HIGH"), Severite("HIGH"), "1.0"),
        Vulnerabilite("CVE-3", [], "desc", Risque("LOW"), Severite("MEDIUM"), "1.0"),
        Vulnerabilite("CVE-4", [], "desc", Risque("LOW"), Severite("LOW"), "1.0"),
    ]
