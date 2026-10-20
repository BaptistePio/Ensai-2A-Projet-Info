
import pytest

from business_object.ComposanteSBOM import ComposanteSBOM


@pytest.fixture
def composante_sbom():
    return ComposanteSBOM(
        "numpy",
        "1.26.0",
        "BSD-3-Clause",
        "abc123",
    )


def test_creation_composante_sbom(composante_sbom):
    assert composante_sbom.nom == "numpy"
    assert composante_sbom.version == "1.26.0"
    assert composante_sbom.licence == "BSD-3-Clause"
    assert composante_sbom.hash_integrite == "abc123"


def test_str_composante_sbom(composante_sbom):
    assert str(composante_sbom) == (
        "numpy (version 1.26.0, licence BSD-3-Clause)"
    )


def test_repr_composante_sbom(composante_sbom):
    assert repr(composante_sbom) == (
        "ComposanteSBOM(nom='numpy', "
        "version='1.26.0', "
        "licence='BSD-3-Clause', "
        "hash_integrite='abc123')"
    )


def test_eq_composantes_identiques(composante_sbom):
    autre = ComposanteSBOM(
        "numpy",
        "1.26.0",
        "BSD-3-Clause",
        "abc123",
    )

    assert composante_sbom == autre


def test_eq_composantes_differentes(composante_sbom):
    autre = ComposanteSBOM(
        "numpy",
        "2.0.0",
        "BSD-3-Clause",
        "abc123",
    )

    assert composante_sbom != autre


def test_eq_autre_type(composante_sbom):
    assert composante_sbom.__eq__("numpy") is NotImplemented
