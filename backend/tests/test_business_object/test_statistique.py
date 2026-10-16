"""Tests unitaires de la classe Statistique (F5).

Lancer avec :  pytest tests/test_business_object/test_statistique.py -v
"""
import unittest
from datetime import UTC, date, datetime, timedelta, timezone

from business_object.journalisation import Journalisation
from business_object.statistique import Statistique

ID = "utilisateur_test"
T = datetime(2026, 10, 6, 17, 10, 8, tzinfo=UTC)
jour_6 = date(2026, 10, 6)
jour_7 = date(2026, 10, 7)
jour_8 = date(2026, 10, 8)


def journal(id_utilisateur=ID, vulnerabilite=4, eco=10, ts=T, decision=True):
    """
    Fabrique une entrée de journal valide qui sera utilisée dans la classe de test
    """
    return Journalisation(id_utilisateur, vulnerabilite, eco, decision, ts)


def stat(**kw):
    """
    Fabrique une Statistique valide qui sera utilisée dans la classe de test
    """
    params = dict(id_utilisateur=ID, nb_soumissions=3, score_vulnerabilite_moyen=4.0,
                  score_eco_moyen=6.0, activite_par_jour={jour_6: 2, jour_7: 1})
    params.update(kw)
    return Statistique(**params)


class TestConstructeur(unittest.TestCase):
    def test_valeurs_conservees(self):
        s = stat()
        self.assertEqual(s.id_utilisateur, ID)
        self.assertEqual(s.nb_soumissions, 3)
        self.assertEqual(s.score_vulnerabilite_moyen, 4.0)
        self.assertEqual(s.score_eco_moyen, 6.0)
        self.assertEqual(s.activite_par_jour, {jour_6: 2, jour_7: 1})

    def test_activite_vide_par_defaut(self):
        s = Statistique(ID, 0, 0.0, 0.0)
        self.assertEqual(s.activite_par_jour, {})

    def test_activite_none_renvoie_activite_vide(self):
        self.assertEqual(stat(activite_par_jour=None).activite_par_jour, {})

    def test_valeurs_a_zero_acceptees(self):
        s = Statistique(ID, 0, 0, 0)
        self.assertEqual((s.nb_soumissions, s.score_vulnerabilite_moyen, s.score_eco_moyen),
                         (0, 0, 0))

    def test_id_vide_refuse(self):
        with self.assertRaises(ValueError):
            stat(id_utilisateur="")

    def test_id_none_refuse(self):
        with self.assertRaises(ValueError):
            stat(id_utilisateur=None)

    def test_nb_soumissions_negatif_refuse(self):
        with self.assertRaises(ValueError):
            stat(nb_soumissions=-1)

    def test_score_vulnerabilite_negatif_refuse(self):
        with self.assertRaises(ValueError):
            stat(score_vulnerabilite_moyen=-0.1)

    def test_score_eco_negatif_refuse(self):
        with self.assertRaises(ValueError):
            stat(score_eco_moyen=-0.1)

    def test_modifier_dict_origine_change_pas_objet(self):
        activite = {jour_6: 2}
        s = stat(activite_par_jour=activite)
        activite[jour_7] = 99
        self.assertEqual(s.activite_par_jour, {jour_6: 2})


class TestLectureSeule(unittest.TestCase):
    def test_attributs_non_modifiables(self):
        s = stat()
        for nom, valeur in [("id_utilisateur", "autre"),
                            ("nb_soumissions", 0),
                            ("score_vulnerabilite_moyen", 0.0),
                            ("score_eco_moyen", 0.0),
                            ("activite_par_jour", {})]:
            with self.subTest(attribut=nom):
                with self.assertRaises(AttributeError):
                    setattr(s, nom, valeur)


class TestActiviteParJour(unittest.TestCase):
    def test_triee_par_date(self):
        s = stat(activite_par_jour={jour_6: 1, jour_7: 2, jour_8: 5})
        self.assertEqual(list(s.activite_par_jour), [jour_6, jour_7, jour_8])

    def test_retourne_une_copie(self):
        s = stat()
        s.activite_par_jour.clear()
        s.activite_par_jour[jour_8] = 42
        self.assertEqual(s.activite_par_jour, {jour_6: 2, jour_7: 1})


class TestObtenirStatistiques(unittest.TestCase):
    def test_retourne_une_statistique(self):
        self.assertIsInstance(Statistique.obtenir_statistiques(ID, [journal()]), Statistique)

    def test_une_seule_entree(self):
        s = Statistique.obtenir_statistiques(ID, [journal(vulnerabilite=7, eco=21)])
        self.assertEqual(s.nb_soumissions, 1)
        self.assertEqual(s.score_vulnerabilite_moyen, 7)
        self.assertEqual(s.score_eco_moyen, 21)
        self.assertEqual(s.activite_par_jour, {jour_6: 1})

    def test_nb_soumissions_egal_au_nombre_d_entrees(self):
        entrees = [journal(), journal(), journal(), journal()]
        self.assertEqual(Statistique.obtenir_statistiques(ID, entrees).nb_soumissions, 4)

    def test_moyennes_calculees_separement(self):
        entrees = [journal(vulnerabilite=4, eco=10), journal(vulnerabilite=0, eco=6), journal(vulnerabilite=8, eco=2)]
        s = Statistique.obtenir_statistiques(ID, entrees)
        self.assertEqual(s.score_vulnerabilite_moyen, 4.0)
        self.assertEqual(s.score_eco_moyen, 6.0)

    def test_moyenne_non_entiere(self):
        entrees = [journal(vulnerabilite=1), journal(vulnerabilite=2), journal(vulnerabilite=2)]
        s = Statistique.obtenir_statistiques(ID, entrees)
        self.assertAlmostEqual(s.score_vulnerabilite_moyen, 5 / 3)

    def test_decision_influence_pas_les_moyennes(self):
        entrees = [journal(vulnerabilite=2, decision=True), journal(vulnerabilite=4, decision=False)]
        self.assertEqual(
            Statistique.obtenir_statistiques(ID, entrees).score_vulnerabilite_moyen, 3)

    def test_activite_plusieurs_soumissions_meme_jour(self):
        entrees = [journal(ts=T), journal(ts=T + timedelta(hours=2))]
        self.assertEqual(Statistique.obtenir_statistiques(ID, entrees).activite_par_jour,
                         {jour_6: 2})

    def test_activite_sur_plusieurs_jours(self):
        entrees = [journal(ts=T), journal(ts=T + timedelta(hours=2)),
                   journal(ts=T + timedelta(days=2))]
        self.assertEqual(Statistique.obtenir_statistiques(ID, entrees).activite_par_jour,
                         {jour_6: 2, jour_8: 1})

    def test_changement_de_jour_a_minuit_utc(self):
        avant = datetime(2026, 10, 6, 23, 59, 59, tzinfo=UTC)
        apres = datetime(2026, 10, 7, 0, 0, 0, tzinfo=UTC)
        s = Statistique.obtenir_statistiques(ID, [journal(ts=avant), journal(ts=apres)])
        self.assertEqual(s.activite_par_jour, {jour_6: 1, jour_7: 1})

    def test_date_avec_fuseau_convertie_en_utc(self):
        # 01h00 le 7 octobre à UTC+2 signifie 23h00 le 6 octobre en UTC
        paris = timezone(timedelta(hours=2))
        ts = datetime(2026, 10, 7, 1, 0, tzinfo=paris)
        s = Statistique.obtenir_statistiques(ID, [journal(ts=ts)])
        self.assertEqual(s.activite_par_jour, {jour_6: 1})

    def test_date_sans_fuseau_utilisee_telle_quelle(self):
        ts = datetime(2026, 10, 6, 23, 0)
        s = Statistique.obtenir_statistiques(ID, [journal(ts=ts)])
        self.assertEqual(s.activite_par_jour, {jour_6: 1})

    def test_liste_vide(self):
        s = Statistique.obtenir_statistiques(ID, [])
        self.assertEqual(s.nb_soumissions, 0)
        self.assertEqual(s.score_vulnerabilite_moyen, 0.0)
        self.assertEqual(s.score_eco_moyen, 0.0)
        self.assertEqual(s.activite_par_jour, {})

    def test_liste_vide_avec_id_vide_refusee(self):
        with self.assertRaises(ValueError):
            Statistique.obtenir_statistiques("", [])

    def test_entree_autre_utilisateur_refusee(self):
        with self.assertRaises(ValueError):
            Statistique.obtenir_statistiques(ID, [journal(id_utilisateur="autre_utilisateur")])

    def test_une_seule_entree_etrangere_parmi_d_autres_refuser(self):
        entrees = [journal(), journal(), journal(id_utilisateur="autre_utilisateur")]
        with self.assertRaises(ValueError):
            Statistique.obtenir_statistiques(ID, entrees)

    def test_liste_entrees_non_modifiee(self):
        entrees = [journal(), journal(ts=T + timedelta(days=1))]
        copie = list(entrees)
        Statistique.obtenir_statistiques(ID, entrees)
        self.assertEqual(entrees, copie)

    def test_resultat_complet(self):
        entrees = [journal(vulnerabilite=4, eco=10, ts=T),
                   journal(vulnerabilite=0, eco=6, ts=T + timedelta(hours=2)),
                   journal(vulnerabilite=8, eco=2, ts=T + timedelta(days=1))]
        self.assertEqual(Statistique.obtenir_statistiques(ID, entrees), stat())


class TestEgalite(unittest.TestCase):
    def test_statistiques_identiques_egales(self):
        self.assertEqual(stat(), stat())

    def test_difference_sur_chaque_champ(self):
        autres = {"id_utilisateur": "autre", "nb_soumissions": 4,
                  "score_vulnerabilite_moyen": 4.5, "score_eco_moyen": 6.5,
                  "activite_par_jour": {jour_6: 3}}
        for champ, valeur in autres.items():
            with self.subTest(champ=champ):
                self.assertNotEqual(stat(), stat(**{champ: valeur}))

    def test_ordre_d_insertion_de_l_activite_sans_importance(self):
        self.assertEqual(stat(activite_par_jour={jour_6: 2, jour_8: 1}),
                         stat(activite_par_jour={jour_8: 1, jour_6: 2}))

    def test_comparaison_avec_autre_type_est_false(self):
        s = stat()
        self.assertFalse(s == 5)
        self.assertFalse(s == ID)
        self.assertFalse(s == None)  # noqa: E711

    def test_not_implemented_pour_autre_type(self):
        self.assertIs(stat().__eq__(5), NotImplemented)


class TestHash(unittest.TestCase):
    def test_statistiques_egales_ont_le_meme_hash(self):
        self.assertEqual(hash(stat()), hash(stat()))

    def test_hash_independant_ordre_activite(self):
        self.assertEqual(hash(stat(activite_par_jour={jour_6: 2, jour_8: 1})),
                         hash(stat(activite_par_jour={jour_8: 1, jour_6: 2})))

    def test_statistiques_differentes_hash_differents(self):
        self.assertNotEqual(hash(stat()), hash(stat(nb_soumissions=4)))
        self.assertNotEqual(hash(stat()), hash(stat(activite_par_jour={jour_6: 3})))

    def test_utilisable_dans_un_set(self):
        self.assertEqual(len({stat(), stat(), stat(nb_soumissions=4)}), 2)

    def test_utilisable_comme_cle_de_dictionnaire(self):
        self.assertEqual({stat(): "utilisateur_test"}[stat()], "utilisateur_test")


class TestCle(unittest.TestCase):
    def test_contient_tous_les_champs_activite_triee(self):
        s = stat(activite_par_jour={jour_8: 1, jour_6: 2})
        self.assertEqual(s._cle(), (ID, 3, 4.0, 6.0, ((jour_6, 2), (jour_8, 1))))

    def test_cle_hachable(self):
        self.assertIsInstance(hash(stat()._cle()), int)


class TestStr(unittest.TestCase):
    def test_format(self): self.assertEqual(
        str(stat()),
        "Statistiques de : utilisateur_test,"
        "Nombre de soumission(s): 3, "
        "vulnérabilité moyenne : 4.00, "
        "éco moyen : 6.00")

    def test_moyennes_arrondies_deux_decimales(self):
        s = stat(score_vulnerabilite_moyen=5 / 3, score_eco_moyen=0.004)
        self.assertIn("vulnérabilité moyenne : 1.67", str(s))
        self.assertIn("éco moyen : 0.00", str(s))

    def test_print_utilise_str(self):
        self.assertIn(ID, f"{stat()}")
