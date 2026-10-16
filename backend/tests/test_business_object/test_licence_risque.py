from business_object.licence_risque import LicenceRisque


def test_obtenir_score_gpl3():
    assert LicenceRisque.obtenir_score("GPL-3.0") == 3


def test_obtenir_score_licence_inconnue():
    assert LicenceRisque.obtenir_score("ihfhvcbdj") == 0


def test_licence_risque_ref():
    resultat = LicenceRisque.licence_risque_ref(3)

    attendu = [{
        "AGPL-3.0": 4,
        "GPL-3.0": 3,
        "GPL-2.0": 3
        },
        {
        "LGPL-3.0": 2
        },
        {
        "Apache-2.0": 1,
        "MIT": 0,
        "BSD-3-Clause": 0
        }]

    assert resultat == attendu
