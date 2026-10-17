from business_object.licence_risque import LicenceRisque


def test_obtenir_score_licence_inconnue():
    assert LicenceRisque.obtenir_score("ihfhvcbdj") == 0


def test_obtenir_score_mit(licence_mit):
    assert LicenceRisque.obtenir_score(licence_mit) == 0


def test_obtenir_score_gpl3(licence_gpl3):
    assert LicenceRisque.obtenir_score(licence_gpl3) == 3


def test_licence_risque_ref():
    resultat = LicenceRisque.licence_risque_ref(3)

    licences_critiques = resultat[0]

    assert "GPL-3.0" in licences_critiques
    assert "AGPL-3.0" in licences_critiques