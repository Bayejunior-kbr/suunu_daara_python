"""
Commandes CLI personnalisées, notamment "flask seed" qui insère des
données de démonstration pour tester le module Maitre (et la relation
avec Classe) sans tout saisir manuellement.
"""
import click
from app.extension import db
from app.models.maitre import Maitre
from app.models.classe import Classe


def register_cli(app):
    @app.cli.command("seed")
    def seed():
        """Insère des maîtres (et classes minimales) de démonstration."""
        demo_maitres = [
            {"matricule": "M001", "prenom": "Ibrahima", "nom": "Diop", "telephone": "771234567"},
            {"matricule": "M002", "prenom": "Fatou", "nom": "Ndiaye", "telephone": "775551122"},
            {"matricule": "M003", "prenom": "Mamadou", "nom": "Ba", "telephone": None},
        ]

        for data in demo_maitres:
            if not db.session.get(Maitre, data["matricule"]):
                db.session.add(Maitre(**data))

        db.session.commit()

        # Une classe rattachée à M001, pour tester la règle
        # "suppression interdite si le maître a des classes".
        if not db.session.get(Classe, "CL-DEB"):
            db.session.add(
                Classe(code="CL-DEB", libelle="Débutants", niveau="1",
                       maitre_matricule="M001")
            )
            db.session.commit()

        click.echo("Données de démonstration insérées (maîtres + 1 classe).")
