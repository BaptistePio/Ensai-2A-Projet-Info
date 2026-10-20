
from datetime import datetime

from business_object.SBOM import SBOM


def test_creation_sbom():
    date = datetime(2026, 10, 20, 14, 30)

    sbom = SBOM(
        1,
        10,
        '{"name": "mon-projet"}',
        date,
        "JSON",
    )

    assert sbom.id_sbom == 1
    assert sbom.id_audit == 10
    assert sbom.contenu == '{"name": "mon-projet"}'
    assert sbom.date_generation == date
    assert sbom.format == "JSON"


def test_str_sbom():
    date = datetime(2026, 10, 20, 14, 30)
    sbom = SBOM(1, 10, "contenu test", date, "JSON")

    assert str(sbom) == (
        "SBOM n°1, audit n°10, "
        "format JSON, généré le 20/10/2026 à 14:30"
    )


def test_repr_sbom():
    date = datetime(2026, 10, 20, 14, 30)
    sbom = SBOM(1, 10, "contenu test", date, "JSON")

    assert repr(sbom) == (
        "SBOM(id_sbom=1, "
        "id_audit=10, "
        "contenu='contenu test', "
        f"date_generation={date!r}, "
        "format='JSON')"
    )


def test_eq_sbom_identiques():
    date = datetime(2026, 10, 20, 14, 30)

    sbom1 = SBOM(1, 10, "contenu test", date, "JSON")
    sbom2 = SBOM(1, 10, "contenu test", date, "JSON")

    assert sbom1 == sbom2


def test_eq_sbom_differents():
    date = datetime(2026, 10, 20, 14, 30)

    sbom1 = SBOM(1, 10, "contenu test", date, "JSON")
    sbom2 = SBOM(2, 10, "contenu test", date, "JSON")

    assert sbom1 != sbom2


def test_eq_sbom_autre_type():
    date = datetime(2026, 10, 20, 14, 30)
    sbom = SBOM(1, 10, "contenu test", date, "JSON")

    assert sbom.__eq__("ceci n'est pas un SBOM") is NotImplemented
