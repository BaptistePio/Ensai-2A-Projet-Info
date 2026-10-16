from business_object.licence import Licence


def test_score_licence():

    licence = Licence(
        "GPL-3.0",
        "GNU GPL v3",
        True
    )

    assert licence.score_licence() == 3
