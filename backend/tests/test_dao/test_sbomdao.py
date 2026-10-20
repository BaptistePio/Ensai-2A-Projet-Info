import os
from datetime import datetime
from unittest.mock import patch

import psycopg2
import pytest
from dao.SBOMdao import SBOMDao

from business_object.SBOM import SBOM
from utils.reset_database import ResetDatabase

ID_AUDIT_AVEC_SBOM = 1
ID_SBOM_EXISTANT = 998
ID_INEXISTANT = 9999999


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    with patch.dict(os.environ, {"SCHEMA": "project_test_dao"}):
        ResetDatabase().run(test_dao=True)
        yield


def test_sauvegarder_ok():
    contenu = '{"bomFormat": "CycloneDX", "test": "sauvegarder_ok"}'
    sbom = SBOM(
        id_sbom=None,
        id_audit=ID_AUDIT_AVEC_SBOM,
        contenu=contenu,
        date_generation=datetime(2026, 9, 20, 10, 0, 0),
        format="CycloneDX",
    )

    SBOMDao().sauvegarder(sbom)

    sboms = SBOMDao().recuperer_par_audit(ID_AUDIT_AVEC_SBOM)
    assert any(s.contenu == contenu for s in sboms)


def test_sauvegarder_ko():
    sbom = SBOM(
        id_sbom=None,
        id_audit=ID_INEXISTANT,
        contenu="{}",
        date_generation=datetime(2026, 9, 20, 10, 0, 0),
        format="CycloneDX",
    )

    with pytest.raises(psycopg2.Error):
        SBOMDao().sauvegarder(sbom)


def test_recuperer_par_audit_existing():
    sboms = SBOMDao().recuperer_par_audit(ID_AUDIT_AVEC_SBOM)

    assert isinstance(sboms, list)
    assert len(sboms) >= 1

    for s in sboms:
        assert isinstance(s, SBOM)
        assert s.id_audit == ID_AUDIT_AVEC_SBOM


def test_recuperer_par_audit_non_existing():
    sboms = SBOMDao().recuperer_par_audit(ID_INEXISTANT)

    assert sboms == []


def test_recuperer_par_audit_ordre_decroissant():
    sboms = SBOMDao().recuperer_par_audit(ID_AUDIT_AVEC_SBOM)

    dates = [s.date_generation for s in sboms]
    assert len(dates) >= 2
    assert dates == sorted(dates, reverse=True)


def test_recuperer_par_id_existing():
    sbom = SBOMDao().recuperer_par_id(ID_SBOM_EXISTANT)

    assert isinstance(sbom, SBOM)
    assert sbom.id_sbom == ID_SBOM_EXISTANT


def test_recuperer_par_id_mappe_les_champs():
    sbom = SBOMDao().recuperer_par_id(ID_SBOM_EXISTANT)

    assert sbom.id_audit == ID_AUDIT_AVEC_SBOM
    assert sbom.contenu == '{"bomFormat": "CycloneDX"}'
    assert sbom.date_generation == datetime(2026, 1, 15, 10, 0, 0)
    assert sbom.format == "CycloneDX"


def test_recuperer_par_id_non_existing():
    sbom = SBOMDao().recuperer_par_id(ID_INEXISTANT)

    assert sbom is None


if __name__ == "__main__":
    pytest.main([__file__])