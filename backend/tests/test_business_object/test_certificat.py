import hashlib
import json
import unittest
from datetime import UTC, datetime, timedelta, timezone

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

from business_object.certificat import Certificat

try:
    from service.verificateur import Verificateur
except ImportError:  # module ou dépendance absente : les tests d'intégration sont ignorés
    Verificateur = None

"""Tests unitaires de la classe Certificat (F5).

TODO(Audit): ces tests seront à revoir quand la classe Audit sera codée.
  - À réécrire : les tests de score_global (la règle de calcul sera décidée dans Audit),
    et tout test dont la signature changerait si le constructeur de Certificat évolue.
  - À ajouter : des tests de validation de score_global (positif, plage...) s'il est contrôlé,
    et un test d'intégration Audit -> QualityGate -> Verificateur.
TODO(Soumission): ajouter des tests sur le format de empreinte_code (SHA-256 hexadécimal,
  64 caractères) si Certificat le valide un jour.
TODO(Utilisateur): ajouter des tests sur le type de id_utilisateur une fois celui de
  Utilisateur.id_utilisateur confirmé.
TODO(persistance): si les certificats sont stockés (DAO), ajouter des tests de
  reconstruction depuis la base, en particulier le maintien de la signature valide.

Lancer avec :  PYTHONPATH=src pytest tests/test_business_object/test_certificat.py -v --noconftest
"""

ID_CERTIFICAT = "cert-1"
ID_UTILISATEUR = "utilisateur_test"
EMPREINTE = hashlib.sha256(b"manifeste du projet").hexdigest()
T = datetime(2026, 10, 24, 12, 0, 0, tzinfo=UTC)


def certificat(**kw):
    """Fabrique un Certificat valide (non signé) ; on surcharge uniquement ce qu'on teste."""
    params = dict(id_certificat=ID_CERTIFICAT, id_utilisateur=ID_UTILISATEUR,
                  empreinte_code=EMPREINTE, date_emission=T,
                  status=Certificat.STATUT_VALIDE, score_global=85)
    params.update(kw)
    return Certificat(**params)


def nouvelle_cle():
    """Paire Ed25519 : (clé privée, clé publique en octets bruts), comme dans Verificateur."""
    privee = Ed25519PrivateKey.generate()
    publique = privee.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return privee, publique


def signer(cert, cle_privee):
    """Même opération que Verificateur.signer_certificat()."""
    cert.signature = cle_privee.sign(cert.message_a_signer())
    return cert


class TestConstructeur(unittest.TestCase):
    def test_valeurs_conservees(self):
        c = certificat()
        self.assertEqual(c.id_certificat, ID_CERTIFICAT)
        self.assertEqual(c.id_utilisateur, ID_UTILISATEUR)
        self.assertEqual(c.empreinte_code, EMPREINTE)
        self.assertEqual(c.date_emission, T)
        self.assertEqual(c.status, "Valide")
        self.assertEqual(c.score_global, 85)

    def test_signature_vide_par_defaut(self):
        self.assertEqual(certificat().signature, b"")

    def test_signature_fournie_conservee(self):
        self.assertEqual(certificat(signature=b"abc").signature, b"abc")

    def test_constante_statut_valide(self):
        self.assertEqual(Certificat.STATUT_VALIDE, "Valide")

    def test_seul_le_statut_valide_est_accepte(self):
        for statut in ["valide", "VALIDE", "Valid", "Refuse", "Refusé", "", None]:
            with self.subTest(status=statut):
                with self.assertRaises(ValueError):
                    certificat(status=statut)


class TestLectureSeule(unittest.TestCase):
    def test_champs_non_modifiables(self):
        c = certificat()
        for nom, valeur in [("id_certificat", "autre"), ("id_utilisateur", "autre"),
                            ("empreinte_code", "0" * 64), ("date_emission", T),
                            ("status", "Valide"), ("score_global", 0)]:
            with self.subTest(attribut=nom):
                with self.assertRaises(AttributeError):
                    setattr(c, nom, valeur)


class TestSignature(unittest.TestCase):
    def test_signature_modifiable(self):
        # Verificateur.signer_certificat() écrit certificat.signature
        c = certificat()
        c.signature = b"nouvelle"
        self.assertEqual(c.signature, b"nouvelle")


class TestMessageASigner(unittest.TestCase):
    def test_est_de_type_bytes(self):
        self.assertIsInstance(certificat().message_a_signer(), bytes)

    def test_contient_les_six_champs_et_pas_la_signature(self):
        donnees = json.loads(certificat(signature=b"abc").message_a_signer())
        self.assertEqual(set(donnees), {"id_certificat", "id_utilisateur", "empreinte_code",
                                        "date_emission", "status", "score_global"})

    def test_valeurs_du_message(self):
        d = json.loads(certificat().message_a_signer())
        self.assertEqual(d["id_certificat"], ID_CERTIFICAT)
        self.assertEqual(d["id_utilisateur"], ID_UTILISATEUR)
        self.assertEqual(d["empreinte_code"], EMPREINTE)
        self.assertEqual(d["date_emission"], T.isoformat())
        self.assertEqual(d["status"], "Valide")
        self.assertEqual(d["score_global"], 85)

    def test_format_exact_du_message(self):
        # Test de non-régression : si ce format change, tous les certificats déjà signés
        # deviennent invérifiables. Ne le modifier que volontairement.
        attendu = (
            '{"date_emission":"2026-10-24T12:00:00+00:00",'
            f'"empreinte_code":"{EMPREINTE}",'
            '"id_certificat":"cert-1","id_utilisateur":"utilisateur_test",'
            '"score_global":85,"status":"Valide"}'
        ).encode("utf-8")
        self.assertEqual(certificat().message_a_signer(), attendu)

    def test_cles_triees(self):
        cles = list(json.loads(certificat().message_a_signer()))
        self.assertEqual(cles, sorted(cles))

    def test_deterministe(self):
        self.assertEqual(certificat().message_a_signer(), certificat().message_a_signer())

    def test_independant_de_la_signature(self):
        c = certificat()
        avant = c.message_a_signer()
        c.signature = b"quelque chose"
        self.assertEqual(c.message_a_signer(), avant)

    def test_change_quand_un_champ_change(self):
        modifications = {"id_certificat": "cert-2", "id_utilisateur": "autre",
                         "empreinte_code": "0" * 64, "date_emission": T + timedelta(seconds=1),
                         "score_global": 86}
        reference = certificat().message_a_signer()
        for champ, valeur in modifications.items():
            with self.subTest(champ=champ):
                self.assertNotEqual(certificat(**{champ: valeur}).message_a_signer(), reference)

    def test_date_normalisee_en_utc(self):
        # même instant exprimé à UTC+2 : le message doit être identique
        paris = T.astimezone(timezone(timedelta(hours=2)))
        self.assertNotEqual(paris.isoformat(), T.isoformat())
        self.assertEqual(certificat(date_emission=paris).message_a_signer(),
                         certificat().message_a_signer())

    def test_date_sans_fuseau_utilisee_telle_quelle(self):
        d = json.loads(certificat(date_emission=datetime(2026, 10, 24, 12, 0)).message_a_signer())
        self.assertEqual(d["date_emission"], "2026-10-24T12:00:00")

    def test_caracteres_accentues_conserves(self):
        message = certificat(id_utilisateur="élodie").message_a_signer()
        self.assertIn("élodie".encode("utf-8"), message)


class TestVerifierAuthenticite(unittest.TestCase):
    def test_certificat_non_signe_refuse(self):
        _, publique = nouvelle_cle()
        self.assertFalse(certificat().verifier_authenticite(publique))

    def test_certificat_signe_accepte(self):
        privee, publique = nouvelle_cle()
        self.assertTrue(signer(certificat(), privee).verifier_authenticite(publique))

    def test_parametre_nomme_cle_publique_signature(self):
        privee, publique = nouvelle_cle()
        c = signer(certificat(), privee)
        self.assertTrue(c.verifier_authenticite(cle_publique_signature=publique))

    def test_contenu_modifie_detecte(self):
        privee, publique = nouvelle_cle()
        signature = signer(certificat(), privee).signature
        modifications = {"id_certificat": "cert-2", "id_utilisateur": "autre",
                         "empreinte_code": hashlib.sha256(b"autre code").hexdigest(),
                         "date_emission": T + timedelta(seconds=1), "score_global": 99}
        for champ, valeur in modifications.items():
            with self.subTest(champ=champ):
                copie = certificat(signature=signature, **{champ: valeur})
                self.assertFalse(copie.verifier_authenticite(publique))

    def test_autre_cle_refusee(self):
        privee, _ = nouvelle_cle()
        _, autre_publique = nouvelle_cle()
        self.assertFalse(signer(certificat(), privee).verifier_authenticite(autre_publique))

    def test_cle_ecdh_x25519_refusee(self):
        # Verificateur a deux clés publiques : celle de l'ECDH ne doit pas valider la signature
        privee, _ = nouvelle_cle()
        ecdh = X25519PrivateKey.generate().public_key().public_bytes(
            serialization.Encoding.Raw, serialization.PublicFormat.Raw)
        self.assertFalse(signer(certificat(), privee).verifier_authenticite(ecdh))

    def test_cle_de_mauvaise_longueur_refusee(self):
        privee, _ = nouvelle_cle()
        c = signer(certificat(), privee)
        for cle in [b"", b"abc", b"x" * 31, b"x" * 33]:
            with self.subTest(longueur=len(cle)):
                self.assertFalse(c.verifier_authenticite(cle))

    def test_signature_corrompue_refusee(self):
        privee, publique = nouvelle_cle()
        c = signer(certificat(), privee)
        c.signature = bytes([c.signature[0] ^ 1]) + c.signature[1:]
        self.assertFalse(c.verifier_authenticite(publique))

    def test_signature_de_mauvaise_longueur_refusee(self):
        _, publique = nouvelle_cle()
        self.assertFalse(certificat(signature=b"abc").verifier_authenticite(publique))

    def test_meme_instant_dans_un_autre_fuseau_accepte(self):
        # cas d'un certificat relu depuis la base avec un autre fuseau
        privee, publique = nouvelle_cle()
        signature = signer(certificat(), privee).signature
        paris = T.astimezone(timezone(timedelta(hours=2)))
        copie = certificat(date_emission=paris, signature=signature)
        self.assertTrue(copie.verifier_authenticite(publique))

    def test_la_verification_ne_modifie_pas_le_certificat(self):
        privee, publique = nouvelle_cle()
        c = signer(certificat(), privee)
        signature = c.signature
        c.verifier_authenticite(publique)
        self.assertEqual(c.signature, signature)


@unittest.skipIf(Verificateur is None, "Verificateur indisponible (import impossible)")
class TestAvecVerificateur(unittest.TestCase):
    """Intégration avec le vrai Verificateur de F1."""

    def test_signer_certificat_stocke_et_renvoie_la_signature(self):
        v = Verificateur()
        c = certificat()
        signature = v.signer_certificat(c)
        self.assertIsInstance(signature, bytes)
        self.assertEqual(c.signature, signature)

    def test_certificat_signe_verifie_avec_cle_publique_signature(self):
        v = Verificateur()
        c = certificat()
        v.signer_certificat(c)
        self.assertTrue(c.verifier_authenticite(v.cle_publique_signature))

    def test_cle_publique_ecdh_du_verificateur_refusee(self):
        v = Verificateur()
        c = certificat()
        v.signer_certificat(c)
        self.assertFalse(c.verifier_authenticite(v.cle_publique))

    def test_autre_verificateur_refuse(self):
        c = certificat()
        Verificateur().signer_certificat(c)
        self.assertFalse(c.verifier_authenticite(Verificateur().cle_publique_signature))

    def test_certificat_modifie_apres_signature_refuse(self):
        v = Verificateur()
        c = certificat()
        v.signer_certificat(c)
        falsifie = certificat(score_global=100, signature=c.signature)
        self.assertFalse(falsifie.verifier_authenticite(v.cle_publique_signature))