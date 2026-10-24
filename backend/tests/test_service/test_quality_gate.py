"""Tests unitaires de la classe QualityGate (F5).

TODO(Audit): ces tests seront à revoir quand la classe Audit sera codée.
  - À réécrire : les tests de score_global (reçu en paramètre, sa règle sera décidée dans
    Audit) et ceux de la signature de generer_certificat si elle change.
  - À ajouter : un test d'intégration Audit -> QualityGate -> Verificateur, et un test
    vérifiant qu'Audit enregistre decision=False dans Journalisation après CertificatRefuse.
TODO(persistance): si l'identifiant du certificat vient un jour de la base de données,
  réécrire les tests sur id_certificat (aujourd'hui un uuid4 généré ici).
TODO(Soumission): ajouter des tests sur le format de empreinte_code s'il est validé.

Lancer avec :  PYTHONPATH=src pytest tests/test_service/test_quality_gate.py -v --noconftest
"""
import hashlib
import unittest
import uuid
from datetime import UTC, datetime, timedelta
from unittest.mock import patch

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from business_object.certificat import Certificat
from service.quality_gate import CertificatRefuse, QualityGate

SEUIL_VULN = 5
SEUIL_CARBONE = 100
ID_UTILISATEUR = "utilisateur_test"
EMPREINTE = hashlib.sha256(b"manifeste du projet").hexdigest()


def gate(vuln=SEUIL_VULN, carbone=SEUIL_CARBONE):
    """Fabrique une QualityGate ; on surcharge uniquement ce qu'on teste."""
    return QualityGate(vuln, carbone)


def generer(g=None, score_vulnerabilite=3, score_eco=50, score_global=80,
            id_utilisateur=ID_UTILISATEUR, empreinte_code=EMPREINTE):
    """Appelle generer_certificat avec des valeurs acceptables par défaut."""
    return (g or gate()).generer_certificat(
        id_utilisateur, empreinte_code, score_vulnerabilite, score_eco, score_global)


class TestConstructeur(unittest.TestCase):
    def test_valeurs_conservees(self):
        g = gate()
        self.assertEqual(g.seuil_vulnerabilite_max, SEUIL_VULN)
        self.assertEqual(g.seuil_carbone_max, SEUIL_CARBONE)

    def test_seuils_a_zero_acceptes(self):
        g = QualityGate(0, 0)
        self.assertEqual((g.seuil_vulnerabilite_max, g.seuil_carbone_max), (0, 0))

    def test_seuil_vulnerabilite_negatif_refuse(self):
        with self.assertRaises(ValueError):
            QualityGate(-1, SEUIL_CARBONE)

    def test_seuil_carbone_negatif_refuse(self):
        with self.assertRaises(ValueError):
            QualityGate(SEUIL_VULN, -1)

    def test_seuils_non_modifiables(self):
        g = gate()
        for nom in ("seuil_vulnerabilite_max", "seuil_carbone_max"):
            with self.subTest(attribut=nom):
                with self.assertRaises(AttributeError):
                    setattr(g, nom, 0)


class TestEvaluer(unittest.TestCase):
    def test_sous_les_deux_seuils_accepte(self):
        self.assertTrue(gate().evaluer(3, 50))

    def test_pile_sur_les_seuils_accepte(self):
        # les seuils sont inclusifs : un score égal au maximum est accepté
        self.assertTrue(gate().evaluer(SEUIL_VULN, SEUIL_CARBONE))

    def test_vulnerabilite_au_dessus_du_seuil_refusee(self):
        self.assertFalse(gate().evaluer(SEUIL_VULN + 1, 50))

    def test_carbone_au_dessus_du_seuil_refuse(self):
        self.assertFalse(gate().evaluer(3, SEUIL_CARBONE + 1))

    def test_les_deux_au_dessus_refuse(self):
        self.assertFalse(gate().evaluer(SEUIL_VULN + 4, SEUIL_CARBONE + 400))

    def test_un_seul_depassement_suffit_au_refus(self):
        g = gate()
        self.assertFalse(g.evaluer(SEUIL_VULN + 1, 0))
        self.assertFalse(g.evaluer(0, SEUIL_CARBONE + 1))

    def test_scores_a_zero_acceptes(self):
        self.assertTrue(gate().evaluer(0, 0))

    def test_seuils_a_zero(self):
        g = QualityGate(0, 0)
        self.assertTrue(g.evaluer(0, 0))
        self.assertFalse(g.evaluer(1, 0))
        self.assertFalse(g.evaluer(0, 1))

    def test_resultat_de_type_bool(self):
        self.assertIsInstance(gate().evaluer(3, 50), bool)
        self.assertIsInstance(gate().evaluer(99, 999), bool)

    def test_score_vulnerabilite_negatif_leve_valueerror(self):
        with self.assertRaises(ValueError):
            gate().evaluer(-1, 50)

    def test_score_eco_negatif_leve_valueerror(self):
        with self.assertRaises(ValueError):
            gate().evaluer(3, -1)


class TestGenererCertificatAccepte(unittest.TestCase):
    def test_retourne_un_certificat(self):
        self.assertIsInstance(generer(), Certificat)

    def test_champs_transmis_au_certificat(self):
        c = generer(id_utilisateur="ana", empreinte_code="a" * 64, score_global=77)
        self.assertEqual(c.id_utilisateur, "ana")
        self.assertEqual(c.empreinte_code, "a" * 64)
        self.assertEqual(c.score_global, 77)  # TODO(Audit): règle de score_global à venir

    def test_statut_valide(self):
        self.assertEqual(generer().status, Certificat.STATUT_VALIDE)

    def test_certificat_non_signe(self):
        # la signature est ajoutée ensuite par Verificateur.signer_certificat()
        self.assertEqual(generer().signature, b"")

    def test_date_emission_du_moment_en_utc(self):
        avant = datetime.now(UTC)
        c = generer()
        apres = datetime.now(UTC)
        self.assertTrue(avant <= c.date_emission <= apres)
        self.assertEqual(c.date_emission.utcoffset(), timedelta(0))

    def test_identifiant_est_un_uuid(self):
        c = generer()
        self.assertEqual(str(uuid.UUID(c.id_certificat)), c.id_certificat)

    def test_identifiants_differents_a_chaque_appel(self):
        g = gate()
        self.assertNotEqual(generer(g).id_certificat, generer(g).id_certificat)

    def test_pile_sur_les_seuils_delivre_un_certificat(self):
        self.assertIsInstance(generer(score_vulnerabilite=SEUIL_VULN, score_eco=SEUIL_CARBONE),
                              Certificat)

    def test_certificat_signable_puis_verifiable(self):
        privee = Ed25519PrivateKey.generate()
        publique = privee.public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        c = generer()
        c.signature = privee.sign(c.message_a_signer())  # comme Verificateur.signer_certificat
        self.assertTrue(c.verifier_authenticite(publique))


class TestGenererCertificatRefuse(unittest.TestCase):
    def test_vulnerabilite_trop_elevee_leve_certificat_refuse(self):
        with self.assertRaises(CertificatRefuse):
            generer(score_vulnerabilite=SEUIL_VULN + 1)

    def test_carbone_trop_eleve_leve_certificat_refuse(self):
        with self.assertRaises(CertificatRefuse):
            generer(score_eco=SEUIL_CARBONE + 1)

    def test_les_deux_trop_eleves_leve_certificat_refuse(self):
        with self.assertRaises(CertificatRefuse):
            generer(score_vulnerabilite=SEUIL_VULN + 4, score_eco=SEUIL_CARBONE + 400)

    def test_message_indique_les_valeurs_et_les_seuils(self):
        # TODO(Audit): à réécrire si Audit attend un autre contenu dans le message de refus
        with self.assertRaises(CertificatRefuse) as ctx:
            generer(score_vulnerabilite=6, score_eco=101)
        message = str(ctx.exception)
        for attendu in ("vulnérabilité 6", "max 5", "carbone 101", "max 100"):
            with self.subTest(attendu=attendu):
                self.assertIn(attendu, message)

    def test_certificat_refuse_n_est_pas_une_valueerror(self):
        # Audit doit pouvoir distinguer un refus (normal) de données invalides (bug)
        self.assertFalse(issubclass(CertificatRefuse, ValueError))
        self.assertTrue(issubclass(CertificatRefuse, Exception))

    def test_score_negatif_leve_valueerror_et_non_certificat_refuse(self):
        with self.assertRaises(ValueError) as ctx:
            generer(score_vulnerabilite=-1)
        self.assertNotIsInstance(ctx.exception, CertificatRefuse)

    def test_la_decision_est_celle_d_evaluer(self):
        g = gate()
        with patch.object(QualityGate, "evaluer", return_value=False):
            with self.assertRaises(CertificatRefuse):
                generer(g, score_vulnerabilite=0, score_eco=0)
        with patch.object(QualityGate, "evaluer", return_value=True):
            self.assertIsInstance(generer(g, score_vulnerabilite=999, score_eco=999),
                                  Certificat)


if __name__ == "__main__":
    unittest.main()