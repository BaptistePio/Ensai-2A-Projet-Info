import pytest

from business_object.licence import Licence


def test_score_licence():

    licence = Licence(
        "GPL-3.0",
        "GNU GPL v3",
        True
    )

    assert licence.score_licence() == 3


def test_score_mit(licence_mit):
    assert licence_mit.score_licence() == 0


def test_score_gpl(licence_gpl):
    assert licence_gpl.score_licence() == 3


def test_score_agpl(licence_agpl):
    assert licence_agpl.score_licence() == 4


def test_licence_inconnue(licence_inconnue):
    with pytest.raises(ValueError):
        licence_inconnue.score_licence()