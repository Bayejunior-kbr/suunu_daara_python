"""
Blueprint du module Maitre.

Couche "Contrôleur" (MVC) : reçoit la requête HTTP, interroge directement
la base via db.session / Model.query (pas de couche repository, conforme
à l'énoncé), valide le formulaire, capture les exceptions métier et
rend le template ou redirige.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extension import db
from app.models.maitre import Maitre
from app.forms.maitre import MaitreForm
from app.exceptions import MaitreIntrouvableException, MaitreDejaExistantException, \
    SuppressionImpossibleException
from app.utils.csv_exporter import exporter_csv
from flask_login import login_required

bp_maitres = Blueprint("maitres", __name__, url_prefix="/maitres")


def _appliquer_recherche(query, q: str):
    """Filtre la query sur nom/prénom/matricule (utilisé par lister et exporter)."""
    if q:
        motif = f"%{q}%"
        query = query.filter(
            Maitre.nom.ilike(motif)
            | Maitre.prenom.ilike(motif)
            | Maitre.matricule.ilike(motif)
        )
    return query


@bp_maitres.route("/")
@login_required
def lister():
    """Liste des maîtres avec recherche optionnelle par nom/prénom/matricule."""
    q = request.args.get("q", "").strip()

    query = _appliquer_recherche(Maitre.query, q)
    maitres = query.order_by(Maitre.nom).all()

    return render_template("maitres/liste.html", maitres=maitres, q=q)


@bp_maitres.route("/nouveau", methods=["GET", "POST"])
def creer():
    """Création d'un nouveau maître."""
    form = MaitreForm()

    if form.validate_on_submit():
        try:
            if db.session.get(Maitre, form.matricule.data):
                raise MaitreDejaExistantException(form.matricule.data)

            maitre = Maitre(
                matricule=form.matricule.data.strip(),
                prenom=form.prenom.data.strip(),
                nom=form.nom.data.strip(),
                telephone=form.telephone.data.strip() if form.telephone.data else None,
            )
            db.session.add(maitre)
            db.session.commit()
            flash(f"Maître « {maitre.nom_complet()} » ajouté avec succès.", "success")
            return redirect(url_for("maitres.lister"))

        except MaitreDejaExistantException as exc:
            db.session.rollback()
            flash(str(exc), "danger")

    return render_template("maitres/formulaire.html", form=form, maitre=None)


@bp_maitres.route("/<matricule>/modifier", methods=["GET", "POST"])
def modifier(matricule):
    """Modification d'un maître existant. Le matricule est en lecture seule."""
    try:
        maitre = db.session.get(Maitre, matricule)
        if not maitre:
            raise MaitreIntrouvableException(matricule)

        form = MaitreForm(obj=maitre)

        if form.validate_on_submit():
            maitre.prenom = form.prenom.data.strip()
            maitre.nom = form.nom.data.strip()
            maitre.telephone = form.telephone.data.strip() if form.telephone.data else None
            db.session.commit()
            flash(f"Maître « {maitre.nom_complet()} » modifié avec succès.", "success")
            return redirect(url_for("maitres.lister"))

        # Le matricule ne doit pas pouvoir être changé : on force sa valeur
        # d'affichage même si le champ est resté vide côté formulaire.
        form.matricule.data = maitre.matricule

        return render_template("maitres/formulaire.html", form=form, maitre=maitre)

    except MaitreIntrouvableException as exc:
        flash(str(exc), "danger")
        return redirect(url_for("maitres.lister"))


@bp_maitres.route("/<matricule>/supprimer", methods=["POST"])
def supprimer(matricule):
    """Suppression d'un maître, interdite s'il encadre encore des classes."""
    try:
        maitre = db.session.get(Maitre, matricule)
        if not maitre:
            raise MaitreIntrouvableException(matricule)

        if maitre.a_des_classes():
            raise SuppressionImpossibleException(
                f"Impossible de supprimer « {maitre.nom_complet()} » : "
                f"il encadre encore {len(maitre.classes)} classe(s). "
                f"Réattribuez ou supprimez d'abord ces classes."
            )

        db.session.delete(maitre)
        db.session.commit()
        flash(f"Maître « {maitre.nom_complet()} » supprimé.", "success")

    except MaitreIntrouvableException as exc:
        flash(str(exc), "danger")
    except SuppressionImpossibleException as exc:
        db.session.rollback()
        flash(str(exc), "danger")

    return redirect(url_for("maitres.lister"))


@bp_maitres.route("/export.csv")
def exporter():
    """Exporte au format CSV la liste affichée (respecte le filtre de recherche)."""
    q = request.args.get("q", "").strip()

    query = _appliquer_recherche(Maitre.query, q)
    maitres = query.order_by(Maitre.nom).all()

    entetes = ["matricule", "prenom", "nom", "telephone", "nombre_classes"]
    lignes = [
        [m.matricule, m.prenom, m.nom, m.telephone or "", len(m.classes)]
        for m in maitres
    ]

    return exporter_csv("maitres.csv", entetes, lignes)
