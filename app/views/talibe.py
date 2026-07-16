from flask import Blueprint, render_template, flash, redirect, url_for, request

from app.extension import db
from app.models.talibe import Talibe
from app.models.classe import Classe
from app.forms.talibe import TalibeForm
from app.exceptions import TalibeIntrouvableException, TalibeDejaExistantException
from app.utils.csv_exporter import exporter_csv

talibes_bp = Blueprint("talibes", __name__, url_prefix="/talibes")


def classe_choix(form):
    """listes deroulant du classe"""
    form.classe_code.choices = [(c.code, c.libelle) for c in Classe.query.order_by(Classe.libelle).all()]


# lister (+ recherche par nom/prenom et filtre par classe, comme demande dans l'enonce)
@talibes_bp.route("/")
def liste():
    q = request.args.get("q", "").strip()
    classe_code = request.args.get("classe", "").strip()

    query = Talibe.query
    if classe_code:
        query = query.filter_by(classe_code=classe_code)
    if q:
        query = query.filter(Talibe.nom.contains(q) | Talibe.prenom.contains(q))

    talibes = query.order_by(Talibe.nom).all()
    classes = Classe.query.order_by(Classe.libelle).all()
    return render_template("talibes/liste.html", talibes=talibes, classes=classes, q=q, classe_code=classe_code)


# ajouter
@talibes_bp.route("/ajouter", methods=["GET", "POST"])
def ajouter():
    form = TalibeForm()
    classe_choix(form)
    # validate_on_submit sa vient directement de Flask-WTF, sa verifie est ce ke tous les champs sont valides
    # et est ce ke l'utilisateur vient de cliquer sur enregistrer
    if form.validate_on_submit():
        try:
            if db.session.get(Talibe, form.matricule.data):
                raise TalibeDejaExistantException(form.matricule.data)

            talibe = Talibe(
                matricule=form.matricule.data,
                nom=form.nom.data,  # .data c'est l'attribut qui contient la vraie valeur que l'utilisateur a saisie ou choisie
                prenom=form.prenom.data,
                date_naissance=form.date_naissance.data,
                nom_tuteur=form.nom_tuteur.data,
                telephone_tuteur=form.telephone_tuteur.data,
                adresse=form.adresse.data,
                classe_code=form.classe_code.data,
            )
            db.session.add(talibe)
            db.session.commit()
            flash("Talibé enregistré avec succès !", "success")  # message temporaire cote serveur (session utilisateur)
            return redirect(url_for("talibes.liste"))
        except TalibeDejaExistantException as exc:
            db.session.rollback()
            flash(str(exc), "danger")
    return render_template("talibes/formulaire.html", form=form, titre="Ajouter un talibé", talibe=None)


@talibes_bp.route("/<matricule>/modifier", methods=["GET", "POST"])
def modifier(matricule):
    talibe = db.session.get(Talibe, matricule)  # cherche le talibe avec son matricule, si introuvable -> exception
    if not talibe:
        try:
            raise TalibeIntrouvableException(matricule)
        except TalibeIntrouvableException as exc:
            flash(str(exc), "danger")
            return redirect(url_for("talibes.liste"))

    form = TalibeForm(obj=talibe)  # cree le formulaire et le pre-remplit avec les donnees du talibe
    classe_choix(form)  # remplit la liste deroulante de classe
    form.matricule.data = talibe.matricule  # le matricule reste affiche mais ne doit pas etre modifiable

    if form.validate_on_submit():  # renvoie vrai si c'est un POST et que les validateurs sont ok
        talibe.nom = form.nom.data  # mettre a jour les donnees avec les nouvelles valeurs saisies
        talibe.prenom = form.prenom.data
        talibe.date_naissance = form.date_naissance.data
        talibe.nom_tuteur = form.nom_tuteur.data
        talibe.telephone_tuteur = form.telephone_tuteur.data
        talibe.adresse = form.adresse.data
        talibe.classe_code = form.classe_code.data

        db.session.commit()  # sauvegarder definitivement les modifications en base de donnees

        flash("Talibé modifié avec succès !", "success")  # message affiche apres la redirection
        return redirect(url_for("talibes.liste"))
    return render_template("talibes/formulaire.html", form=form, titre="Modifier un talibé", talibe=talibe)


@talibes_bp.route("/<matricule>/supprimer", methods=["POST"])
def supprimer(matricule):
    try:
        talibe = db.session.get(Talibe, matricule)  # recuperer le talibe a supprimer avec son matricule
        if not talibe:
            raise TalibeIntrouvableException(matricule)

        db.session.delete(talibe)  # marquer pour suppression (cascade -> ses progressions aussi)
        db.session.commit()  # supprimer reellement en base de donnees
        flash("Talibé supprimé avec succès (ainsi que ses progressions) !", "success")
    except TalibeIntrouvableException as exc:
        flash(str(exc), "danger")

    return redirect(url_for("talibes.liste"))


@talibes_bp.route("/export.csv")  # URL /talibes/export.csv
def export_csv():
    """Exporte au format CSV la liste affichee (respecte le filtre de recherche / classe)."""
    q = request.args.get("q", "").strip()
    classe_code = request.args.get("classe", "").strip()

    query = Talibe.query
    if classe_code:
        query = query.filter_by(classe_code=classe_code)
    if q:
        query = query.filter(Talibe.nom.contains(q) | Talibe.prenom.contains(q))

    talibes = query.order_by(Talibe.nom).all()

    entetes = ["matricule", "prenom", "nom", "dateNaissance", "nom_tuteur", "telephone_tuteur", "adresse", "classe"]
    lignes = [
        [
            t.matricule, t.prenom, t.nom, t.date_naissance,
            t.nom_tuteur, t.telephone_tuteur, t.adresse,
            t.classe.libelle if t.classe else "",
        ]
        for t in talibes
    ]
    return exporter_csv("talibes.csv", entetes, lignes)
