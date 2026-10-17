import pytest


def test_nom_package(package_django):
    assert package_django.nom == "django"


def test_version_package(package_django):
    assert package_django.version == "4.2.0"


def test_ecosysteme_package(package_django):
    assert package_django.ecosysteme == "PyPI"


def test_licence_package(package_django):
    assert package_django.licence.idspdx == "MIT"