"""
Tests du module Maitre : couvrent lister, rechercher, ajouter, modifier,
supprimer, exporter CSV, ainsi que les règles métier (unicité du
matricule, interdiction de suppression si le maître a des classes).
"""
from app.models.maitre import Maitre
from app.models.classe import Classe


def _creer_maitre(client, matricule="M100", prenom="Awa", nom="Sow", telephone="770001122"):
    return client.post(
        "/maitres/nouveau",
        data={"matricule": matricule, "prenom": prenom, "nom": nom, "telephone": telephone},
        follow_redirects=True,
    )


class TestListerEtRechercher:
    def test_liste_vide_au_depart(self, client):
        resp = client.get("/maitres/")
        assert resp.status_code == 200
        assert "Aucun maître trouvé".encode() in resp.data

    def test_liste_affiche_les_maitres_crees(self, client, db):
        db.session.add(Maitre(matricule="M001", prenom="Ibrahima", nom="Diop"))
        db.session.add(Maitre(matricule="M002", prenom="Fatou", nom="Ndiaye"))
        db.session.commit()

        resp = client.get("/maitres/")
        assert b"Diop" in resp.data
        assert b"Ndiaye" in resp.data

    def test_recherche_par_nom(self, client, db):
        db.session.add(Maitre(matricule="M001", prenom="Ibrahima", nom="Diop"))
        db.session.add(Maitre(matricule="M002", prenom="Fatou", nom="Ndiaye"))
        db.session.commit()

        resp = client.get("/maitres/?q=Diop")
        assert b"Diop" in resp.data
        assert b"Ndiaye" not in resp.data

    def test_recherche_sans_resultat(self, client, db):
        db.session.add(Maitre(matricule="M001", prenom="Ibrahima", nom="Diop"))
        db.session.commit()

        resp = client.get("/maitres/?q=Inexistant")
        assert "Aucun maître trouvé".encode() in resp.data


class TestCreation:
    def test_creation_reussie(self, client, db):
        resp = _creer_maitre(client)
        assert resp.status_code == 200
        assert db.session.get(Maitre, "M100") is not None
        assert "ajouté avec succès".encode() in resp.data

    def test_creation_matricule_deja_existant_rejetee(self, client, db):
        _creer_maitre(client, matricule="M100")
        resp = _creer_maitre(client, matricule="M100", prenom="Autre", nom="Personne")

        assert "existe déjà".encode() in resp.data
        # Un seul maître avec ce matricule doit exister (pas d'écrasement)
        assert Maitre.query.filter_by(matricule="M100").count() == 1

    def test_creation_champs_obligatoires_manquants(self, client, db):
        resp = client.post(
            "/maitres/nouveau",
            data={"matricule": "", "prenom": "", "nom": "", "telephone": ""},
        )
        assert resp.status_code == 200  # réaffiche le formulaire
        assert db.session.get(Maitre, "") is None


class TestModification:
    def test_modification_reussie(self, client, db):
        _creer_maitre(client, matricule="M100", nom="Sow")

        resp = client.post(
            "/maitres/M100/modifier",
            data={"matricule": "M100", "prenom": "Awa", "nom": "Ba", "telephone": "770009999"},
            follow_redirects=True,
        )
        maitre = db.session.get(Maitre, "M100")
        assert maitre.nom == "Ba"
        assert "modifié avec succès".encode() in resp.data

    def test_modification_matricule_inexistant(self, client):
        resp = client.get("/maitres/INCONNU/modifier", follow_redirects=True)
        assert "Aucun maître trouvé".encode() in resp.data


class TestSuppression:
    def test_suppression_reussie(self, client, db):
        _creer_maitre(client, matricule="M100")

        resp = client.post("/maitres/M100/supprimer", follow_redirects=True)
        assert db.session.get(Maitre, "M100") is None
        assert "supprimé".encode() in resp.data

    def test_suppression_interdite_si_classes_rattachees(self, client, db):
        _creer_maitre(client, matricule="M100")
        db.session.add(Classe(code="CL-1", libelle="Debutants", maitre_matricule="M100"))
        db.session.commit()

        resp = client.post("/maitres/M100/supprimer", follow_redirects=True)

        # Le maître doit toujours exister : la suppression a été bloquée
        assert db.session.get(Maitre, "M100") is not None
        assert "Impossible de supprimer".encode() in resp.data

    def test_suppression_matricule_inexistant(self, client):
        resp = client.post("/maitres/INCONNU/supprimer", follow_redirects=True)
        assert "Aucun maître trouvé".encode() in resp.data


class TestExportCSV:
    def test_export_csv_contenu(self, client, db):
        db.session.add(Maitre(matricule="M001", prenom="Ibrahima", nom="Diop", telephone="770000000"))
        db.session.commit()

        resp = client.get("/maitres/export.csv")
        assert resp.status_code == 200
        assert resp.headers["Content-Type"].startswith("text/csv")
        assert "attachment" in resp.headers["Content-Disposition"]

        contenu = resp.data.decode("utf-8")
        assert "matricule,prenom,nom,telephone,nombre_classes" in contenu
        assert "M001,Ibrahima,Diop,770000000,0" in contenu

    def test_export_csv_respecte_le_filtre(self, client, db):
        db.session.add(Maitre(matricule="M001", prenom="Ibrahima", nom="Diop"))
        db.session.add(Maitre(matricule="M002", prenom="Fatou", nom="Ndiaye"))
        db.session.commit()

        resp = client.get("/maitres/export.csv?q=Diop")
        contenu = resp.data.decode("utf-8")
        assert "Diop" in contenu
        assert "Ndiaye" not in contenu


class TestModeleMaitre:
    def test_nom_complet(self, db):
        m = Maitre(matricule="M001", prenom="Ibrahima", nom="Diop")
        assert m.nom_complet() == "Ibrahima Diop"

    def test_a_des_classes_faux_par_defaut(self, db):
        m = Maitre(matricule="M001", prenom="Ibrahima", nom="Diop")
        db.session.add(m)
        db.session.commit()
        assert m.a_des_classes() is False

    def test_a_des_classes_vrai_si_relation(self, db):
        m = Maitre(matricule="M001", prenom="Ibrahima", nom="Diop")
        db.session.add(m)
        db.session.commit()
        db.session.add(Classe(code="CL-1", libelle="Debutants", maitre_matricule="M001"))
        db.session.commit()
        assert m.a_des_classes() is True
