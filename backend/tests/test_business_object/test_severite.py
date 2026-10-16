from business_object.severite import Severite


def test_score_critical():
    assert Severite("CRITICAL").score() == 4


def test_score_high():
    assert Severite("HIGH").score() == 3


def test_score_medium():
    assert Severite("MEDIUM").score() == 2


def test_score_low():
    assert Severite("LOW").score() == 1


def test_score_inconnu():
    assert Severite("jhdfvjez").score() == 0