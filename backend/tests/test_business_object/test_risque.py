from risque import Risque


def test_score_high():
    assert Risque("HIGH").score_risque() == 3


def test_score_medium():
    assert Risque("MedIUm").score_risque() == 2


def test_score_low():
    assert Risque("low").score_risque() == 1


def test_score_inconnu():
    assert Risque("hkfsbvifb").score_risque() == 0
