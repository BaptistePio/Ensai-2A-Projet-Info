import unittest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from business_object.journalisation import Journalisation
from dao.historique_dao import Historique

# Chemin où le DAO a importé get_connection (à adapter si le fichier change de nom)
CIBLE = "dao.connexion_bdd_ex.connection"
#Est ce la bonne fonction a relié ?

T = datetime(2026, 10, 6, 17, 10, 8, tzinfo=timezone.utc)
T2 = T + timedelta(days=1)


def renvoie_ligne(id_utilisateur="utilisateur_test", vuln=3, eco=12, decision=True, ts=T):
    return (id_utilisateur, vuln, eco, decision, ts)


class BaseTestDAO(unittest.TestCase):
    """Met en place une fausse connexion avant chaque test."""

    def setUp(self):
        patcher = patch(CIBLE)
        self.connection = patcher.start()
        self.addCleanup(patcher.stop)
        self.contexte = self.connection.return_value
        self.conn = self.contexte.__enter__.return_value
        self.curseur = self.conn.cursor.return_value.__enter__.return_value
        self.curseur.fetchall.return_value = []
        self.dao = Historique()

    def requete_et_params(self):
        args = self.curseur.execute.call_args.args
        return args[0], args[1]


class TestInit(unittest.TestCase):
    def test_instanciable_sans_argument(self):
        self.assertIsInstance(Historique(), Historique)


class TestEnregistrerJournal(BaseTestDAO):
    def enregistrer(self, **kw):
        params = dict(id_utilisateur="utilisateur_test", timestamp=T,
                      score_vulnerabilite=3, score_eco=12, decision=True)
        params.update(kw)
        return self.dao.historique.enregistrer_journal(**params)

    def test_execute_un_insert_dans_journalisation(self):
        self.enregistrer()
        self.curseur.execute.assert_called_once()
        sql, _ = self.requete_et_params()
        self.assertIn("INSERT INTO journalisation", sql)

    def test_parametres_dans_le_bon_ordre(self):
        self.enregistrer()
        _, params = self.requete_et_params()
        self.assertEqual(params, ("utilisateur_test", T, 3, 12, True))

    def test_decision_false(self):
        self.enregistrer(decision=False)
        _, params = self.requete_et_params()
        self.assertIs(params[4], False)

    def test_commit_appele_une_fois(self):
        self.enregistrer()
        self.conn.commit.assert_called_once()

    def test_commit_apres_execute(self):
        ordre = []
        self.curseur.execute.side_effect = lambda *a, **k: ordre.append("execute")
        self.conn.commit.side_effect = lambda: ordre.append("commit")
        self.enregistrer()
        self.assertEqual(ordre, ["execute", "commit"])

    def test_une_seule_connexion_ouverte_et_refermee(self):
        self.enregistrer()
        self.connection.assert_called_once()
        self.contexte.__exit__.assert_called_once()

    def test_retourne_none(self):
        self.assertIsNone(self.enregistrer())

    def test_timestamp_none_utilise_la_date_du_moment_en_utc(self):
        avant = datetime.now(timezone.utc)
        self.enregistrer(timestamp=None)
        apres = datetime.now(timezone.utc)
        _, params = self.requete_et_params()
        self.assertTrue(avant <= params[1] <= apres)

    def test_timestamp_par_defaut_a_un_fuseau_utc(self):
        self.enregistrer(timestamp=None)
        _, params = self.requete_et_params()
        self.assertIsNotNone(params[1].tzinfo)
        self.assertEqual(params[1].utcoffset(), timedelta(0))

    def test_timestamp_fourni_n_est_pas_modifie(self):
        self.enregistrer(timestamp=T2)
        _, params = self.requete_et_params()
        self.assertIs(params[1], T2)

    def test_id_vide_refuse_sans_toucher_la_base(self):
        with self.assertRaises(ValueError):
            self.enregistrer(id_utilisateur="")
        self.connection.assert_not_called()

    def test_id_none_refuse_sans_toucher_la_base(self):
        with self.assertRaises(ValueError):
            self.enregistrer(id_utilisateur=None)
        self.connection.assert_not_called()

    def test_score_vulnerabilite_negatif_refuse_sans_toucher_la_base(self):
        with self.assertRaises(ValueError):
            self.enregistrer(score_vulnerabilite=-1)
        self.connection.assert_not_called()

    def test_score_eco_negatif_refuse_sans_toucher_la_base(self):
        with self.assertRaises(ValueError):
            self.enregistrer(score_eco=-1)
        self.connection.assert_not_called()

    def test_donnee_invalide_declenche_execute_commit_rien(self):
        with self.assertRaises(ValueError):
            self.enregistrer(score_eco=-1)
        self.curseur.execute.assert_not_called()
        self.conn.commit.assert_not_called()

    def test_scores_zero_acceptes(self):
        self.enregistrer(score_vulnerabilite=0, score_eco=0)
        _, params = self.requete_et_params()
        self.assertEqual((params[2], params[3]), (0, 0))

    def test_erreur_sql_propagee_et_pas_de_commit(self):
        self.curseur.execute.side_effect = RuntimeError("Base Indisponible")
        with self.assertRaises(RuntimeError):
            self.enregistrer()
        self.conn.commit.assert_not_called()

    def test_connexion_impossible_propagee(self):
        self.connection.side_effect = ConnectionError("Pas de réseau")
        with self.assertRaises(ConnectionError):
            self.enregistrer()


class TestTrouverUtilisateur(BaseTestDAO):
    def test_requete_filtre_sur_l_utilisateur_du_plus_recent_au_plus_ancien(self):
        self.dao.trouver_utilisateur("utilisateur_test")
        sql, params = self.requete_et_params()
        self.assertIn("WHERE id_utilisateur = %s", sql)
        self.assertIn("ORDER BY timestamp DESC", sql)
        self.assertEqual(params, ("utilisateur_test",))

    def test_aucune_ligne_donne_liste_vide(self):
        self.assertEqual(self.dao.trouver_utilisateur("inconnu"), [])

    def test_une_ligne_devient_une_journalisation(self):
        self.curseur.fetchall.return_value = [renvoie_ligne()]
        resultat = self.dao.trouver_utilisateur("utilisateur_test")
        self.assertEqual(len(resultat), 1)
        self.assertIsInstance(resultat[0], Journalisation)
        self.assertEqual(resultat[0],
                         Journalisation("utilisateur_test", 3, 12, True, T))

    def test_plusieurs_lignes_ordre_conserve(self):
        self.curseur.fetchall.return_value = [renvoie_ligne(ts=T2, vuln=5), renvoie_ligne(ts=T, vuln=1)]
        resultat = self.dao.trouver_utilisateur("utilisateur_test")
        self.assertEqual([e.timestamp for e in resultat], [T2, T])

    def test_identifiant_passe_en_parametre_pas_dans_le_sql(self):
        piege = "x'; DROP TABLE journalisation; --"
        self.dao.trouver_utilisateur(piege)
        sql, params = self.requete_et_params()
        self.assertNotIn(piege, sql)
        self.assertEqual(params, (piege,))

    def test_erreur_sql_propagee(self):
        self.curseur.execute.side_effect = RuntimeError("Base Indisponible")
        with self.assertRaises(RuntimeError):
            self.dao.trouver_utilisateur("utilisateur_test")


class TestTrouverPeriode(BaseTestDAO):
    def test_requete_entre_deux_dates_du_plus_ancien_au_plus_recent(self):
        self.dao.trouver_periode(T, T2)
        sql, params = self.requete_et_params()
        self.assertIn("BETWEEN %s AND %s", sql)
        self.assertIn("ORDER BY timestamp ASC", sql)
        self.assertEqual(params, (T, T2))

    def test_aucune_ligne_donne_liste_vide(self):
        self.assertEqual(self.dao.trouver_periode(T, T2), [])

    def test_lignes_converties_en_journalisation(self):
        self.curseur.fetchall.return_value = [renvoie_ligne(ts=T), renvoie_ligne(ts=T2, decision=False)]
        resultat = self.dao.trouver_periode(T, T2)
        self.assertEqual(len(resultat), 2)
        self.assertTrue(all(isinstance(e, Journalisation) for e in resultat))
        self.assertEqual([e.decision for e in resultat], [True, False])

    def test_erreur_sql_propagee(self):
        self.curseur.execute.side_effect = RuntimeError("Base Indisponible")
        with self.assertRaises(RuntimeError):
            self.dao.trouver_periode(T, T2)


class TestRepertorierStatut(BaseTestDAO):
    def test_requete_filtre_sur_la_decision(self):
        self.dao.repertorier_statut(True)
        sql, params = self.requete_et_params()
        self.assertIn("WHERE decision = %s", sql)
        self.assertEqual(params, (True,))

    def test_refuses_transmis_avec_false(self):
        self.dao.repertorier_statut(False)
        _, params = self.requete_et_params()
        self.assertEqual(params, (False,))

    def test_aucune_ligne_renvoie_liste_vide(self):
        self.assertEqual(self.dao.repertorier_statut(True), [])

    def test_lignes_converties_en_journalisation(self):
        self.curseur.fetchall.return_value = [renvoie_ligne(decision=False)]
        resultat = self.dao.repertorier_statut(False)
        self.assertEqual(len(resultat), 1)
        self.assertFalse(resultat[0].decision)

    def test_erreur_sql_propagee(self):
        self.curseur.execute.side_effect = RuntimeError("Base Indisponible")
        with self.assertRaises(RuntimeError):
            self.dao.repertorier_statut(True)


class TestTransfoSqlEnJournalisation(BaseTestDAO):
    def test_requete_et_parametres_transmis_a_execute(self):
        self.dao.transfo_sql_en_journalisation("SELECT 1 WHERE x = %s", (42,))
        self.curseur.execute.assert_called_once_with("SELECT 1 WHERE x = %s", (42,))

    def test_correspondance_des_colonnes(self):
        self.curseur.fetchall.return_value = [("ana", 7, 21, False, T2)]
        e = self.dao.transfo_sql_en_journalisation("SELECT", ())[0]
        self.assertEqual(e.id_utilisateur, "ana")
        self.assertEqual(e.score_vulnerabilite, 7)
        self.assertEqual(e.score_eco, 21)
        self.assertIs(e.decision, False)
        self.assertEqual(e.timestamp, T2)

    def test_aucune_ligne_donne_liste_vide(self):
        self.assertEqual(self.dao.transfo_sql_en_journalisation("SELECT", ()), [])

    def test_plusieurs_lignes_convertie_dans_l_ordre(self):
        self.curseur.fetchall.return_value = [renvoie_ligne("a"), renvoie_ligne("b"), renvoie_ligne("c")]
        resultat = self.dao.transfo_sql_en_journalisation("SELECT", ())
        self.assertEqual([e.id_utilisateur for e in resultat], ["a", "b", "c"])

    def test_ligne_invalide_en_base_leve_valueerror(self):
        self.curseur.fetchall.return_value = [renvoie_ligne(eco=-5)]
        with self.assertRaises(ValueError):
            self.dao.transfo_sql_en_journalisation("SELECT", ())

    def test_connexion_refermee_apres_lecture(self):
        self.dao.transfo_sql_en_journalisation("SELECT", ())
        self.contexte.__exit__.assert_called_once()

    def test_connexion_refermee_meme_en_cas_d_erreur(self):
        self.curseur.execute.side_effect = RuntimeError("boum")
        with self.assertRaises(RuntimeError):
            self.dao.transfo_sql_en_journalisation("SELECT", ())
        self.contexte.__exit__.assert_called_once()

    def test_pas_de_commit_en_lecture(self):
        self.dao.transfo_sql_en_journalisation("SELECT", ())
        self.conn.commit.assert_not_called()


if __name__ == "__main__":
    unittest.main()