import json
import unittest
from datetime import datetime, timezone, timedelta
 
from business_object.journalisation import Journalisation
 
T = datetime(2026, 10, 6, 17, 10, 8, tzinfo=timezone.utc)
 
 
def entree(**kw): #proposé par Claude, utile ??
    """
    Fabrique une entrée valide ; on surcharge uniquement ce qu'on teste.
    """
    params = dict(id_utilisateur="utilisateur_test", score_vulnerabilite=3,
                  score_eco=12, decision=True, timestamp=T)
    params.update(kw)
    return Journalisation(**params)
 
 
class TestConstructeur(unittest.TestCase):
    def test_entree_valide_conserve_les_valeurs(self):
        j = entree()
        self.assertEqual(j.id_utilisateur, "utilisateur_test")
        self.assertEqual(j.score_vulnerabilite, 3)
        self.assertEqual(j.score_eco, 12)
        self.assertTrue(j.decision)
        self.assertEqual(j.timestamp, T)
 
    def test_timestamp_automatique_si_absent(self):
        avant = datetime.now(timezone.utc)
        j = Journalisation("utilisateur_test", 3, 12, True)
        apres = datetime.now(timezone.utc)
        self.assertTrue(avant <= j.timestamp <= apres)
 
    def test_timestamp_en_utc(self):
        j = Journalisation("utilisateur_test", 3, 12, True)
        self.assertEqual(j.timestamp.utcoffset(), timedelta(0))
 
    def test_decision_false_acceptee(self):
        self.assertFalse(entree(decision=False).decision)
 
    def test_id_vide_refuse(self):
        with self.assertRaises(ValueError):
            entree(id_utilisateur="")
 
    def test_id_none_refuse(self):
        with self.assertRaises(ValueError):
            entree(id_utilisateur=None)
    
    def test_scores_a_zero_acceptes(self):
        j = entree(score_vulnerabilite=0, score_eco=0)
        self.assertEqual((j.score_vulnerabilite, j.score_eco), (0, 0))
 
    def test_score_eco_negatif_refuse(self):
        with self.assertRaises(ValueError):
            entree(score_eco=-1)
        
    def test_score_vulnerabilite_negatif_refuse(self):
        with self.assertRaises(ValueError):
            entree(score_vulnerabilite=-1)
    
class TestLectureAttributs(unittest.TestCase):
    def test_attributs_non_modifiables(self):
        j = entree()
        for nom, valeur in [("id_utilisateur", "autre"), ("score_vulnerabilite", 0),
                            ("score_eco", 0), ("decision", False), ("timestamp", T)]:
            with self.subTest(attribut=nom):
                with self.assertRaises(AttributeError):
                    setattr(j, nom, valeur)

class TestVersDict(unittest.TestCase):
    def test_contient_exactement_les_cinq_cles(self):
        self.assertEqual(set(entree().vers_dict()),
                         {"id_utilisateur",
                          "timestamp",
                          "score_vulnerabilite",
                          "score_eco",
                          "decision"})
 
    def test_valeurs(self):
        d = entree().vers_dict()
        self.assertEqual(d["id_utilisateur"], "utilisateur_test")
        self.assertEqual(d["score_vulnerabilite"], 3)
        self.assertEqual(d["score_eco"], 12)
        self.assertIs(d["decision"], True)
 
    def test_timestamp_texte_iso(self):
        d = entree().vers_dict()
        self.assertIsInstance(d["timestamp"], str)
        self.assertEqual(d["timestamp"], T.isoformat())
 
    def test_serialisable_en_json(self):
        texte = json.dumps(entree().vers_dict())
        self.assertIsInstance(texte, str)
 
    def test_modifier_le_dict_ne_change_pas_l_entree(self):
        j = entree()
        d = j.vers_dict()
        d["score_eco"] = 999
        self.assertEqual(j.score_eco, 12)

class TestDepuisDict(unittest.TestCase):
    def test_aller_retour_identique(self):
        j = entree()
        self.assertEqual(Journalisation.depuis_dict(j.vers_dict()), j)
 
    def test_aller_retour_avec_decision_false(self):
        j = entree(decision=False)
        self.assertEqual(Journalisation.depuis_dict(j.vers_dict()), j)
 
    def test_aller_retour_via_json(self):
        j = entree()
        relu = json.loads(json.dumps(j.vers_dict()))
        self.assertEqual(Journalisation.depuis_dict(relu), j)
 
    def test_timestamp_redevient_un_datetime(self):
        j = Journalisation.depuis_dict(entree().vers_dict())
        self.assertIsInstance(j.timestamp, datetime)
        self.assertEqual(j.timestamp, T)
 
    def test_scores_convertis_en_int(self):
        d = entree().vers_dict()
        d["score_vulnerabilite"], d["score_eco"] = "6", "7"
        j = Journalisation.depuis_dict(d)
        self.assertEqual((j.score_vulnerabilite, j.score_eco), (6, 7))
        self.assertIsInstance(j.score_vulnerabilite, int)
 
    def test_retourne_une_journalisation(self):
        self.assertIsInstance(Journalisation.depuis_dict(entree().vers_dict()),
                              Journalisation)
 
    def test_cle_manquante_leve_keyerror(self):
        for cle in ["id_utilisateur",
                    "timestamp",
                    "score_vulnerabilite",
                    "score_eco", 
                    "decision"]:
            with self.subTest(cle_manquante=cle):
                d = entree().vers_dict()
                del d[cle]
                with self.assertRaises(KeyError):
                    Journalisation.depuis_dict(d)
 
    def test_timestamp_invalide_leve_valueerror(self):
        d = entree().vers_dict()
        d["timestamp"] = "pas une date"
        with self.assertRaises(ValueError):
            Journalisation.depuis_dict(d)
 
    def test_valeurs_invalides_refusees(self):
        d = entree().vers_dict()
        d["score_eco"] = -1 
        with self.assertRaises(ValueError):
            Journalisation.depuis_dict(d)
    
    def test_score_vulnerabilite_invalide_refuse(self):
        d = entree().vers_dict()
        d["score_vulnerabilite"] = -1
        with self.assertRaises(ValueError):
            Journalisation.depuis_dict(d)

class TestEgalite(unittest.TestCase):
    def test_entrees_identiques_egales(self):
        self.assertEqual(entree(), entree())
 
    def test_difference_sur_chaque_champ(self):
        autres = {"id_utilisateur": "autre",
                  "score_vulnerabilite": 4,
                  "score_eco": 13,
                  "decision": False,
                  "timestamp": T + timedelta(seconds=1)}
        for champ, valeur in autres.items():
            with self.subTest(champ=champ):
                self.assertNotEqual(entree(), entree(**{champ: valeur}))
 
    def test_comparaison_avec_autre_type_renvoie_faux(self):
        j = entree()
        self.assertFalse(j == 5)
        self.assertFalse(j == "utilisateur_test")
        self.assertFalse(j == j.vers_dict())
        self.assertFalse(j == None)
 
    def test_not_implemented_pour_autre_type(self):
        self.assertIs(entree().__eq__(5), NotImplemented)
 
class TestStr(unittest.TestCase):
    def test_format_certifie(self):
        self.assertEqual(
            str(entree()),
            "[2026-10-06 17:10] utilisateur_test vulnerabilite=3 eco=12 -> Certifié")
 
    def test_format_refuse(self):
        self.assertEqual(
            str(entree(decision=False)),
            "[2026-10-06 17:10] utilisateur_test vulnerabilite=3 eco=12 -> Refusé")
 
    def test_print_utilise_str(self):
        self.assertIn("utilisateur_test", f"{entree()}")
 
class TestHash(unittest.TestCase):
    def test_entrees_egales_ont_hash_egal(self):
        self.assertEqual(hash(entree()), hash(entree()))
 
    def test_entrees_differentes_ont_hash_differents(self):
        self.assertNotEqual(hash(entree()), hash(entree(score_eco=13)))
        self.assertNotEqual(hash(entree()), hash(entree(id_utilisateur="autre")))
 
    def test_dedoublonner_entrees_journal(self):
        # deux doublons + une entrée différente -> 2 éléments
        self.assertEqual(len({entree(), entree(), entree(decision=False)}), 2)
 
    def test_utilisable_comme_cle_de_dictionnaire(self):
        d = {entree(): "audit_1"}
        self.assertEqual(d[entree()], "audit_1")
 
    def test_hash_stable_apres_aller_retour(self):
        j = entree()
        self.assertEqual(hash(Journalisation.depuis_dict(j.vers_dict())), hash(j))
 