from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from app.extension import db
from app.models.progression import Progression
from app.models.talibe import Talibe
from app.forms.progression import ProgressionForm
from app.exceptions import ProgressionIntrouvableException
from app.utils.csv_exporter import exporter_progressions_csv


bp_progressions = Blueprint(
    "progressions",
    __name__,
    url_prefix="/progressions"
)


# ==========================
# LISTE + RECHERCHE
# ==========================

@bp_progressions.route("/")
def lister():

    recherche = request.args.get("q")
    talibe_matricule = request.args.get("talibe", "").strip()

    progressions = Progression.query.join(Talibe)

    if recherche:
        progressions = progressions.filter(
            db.or_(
                Progression.sourate.ilike(f"%{recherche}%"),
                Talibe.prenom.ilike(f"%{recherche}%"),
                Talibe.nom.ilike(f"%{recherche}%")
            )
        )

    # filtre par talibé (demandé par l'énoncé, en plus de la recherche texte)
    if talibe_matricule:
        progressions = progressions.filter(Progression.talibe_matricule == talibe_matricule)

    progressions = progressions.all()

    talibes = Talibe.query.order_by(Talibe.nom).all()

    return render_template(
        "progressions/liste.html",
        progressions=progressions,
        talibes=talibes,
        talibe_matricule=talibe_matricule,
        q=recherche or ""
    )


# ==========================
# AJOUT
# ==========================

@bp_progressions.route("/nouveau", methods=["GET", "POST"])
def creer():

    form = ProgressionForm()

    form.talibe_matricule.choices = [
        (
            t.matricule,
            f"{t.prenom} {t.nom}"
        )
        for t in Talibe.query.all()
    ]


    if form.validate_on_submit():

        progression = Progression(
            sourate=form.sourate.data,
            nombre_versets=form.nombre_versets.data,
            date_evaluation=form.date_evaluation.data,
            observations=form.observations.data,
            talibe_matricule=form.talibe_matricule.data
        )


        db.session.add(progression)
        db.session.commit()


        flash(
            "Progression ajoutée",
            "success"
        )


        return redirect(
            url_for("progressions.lister")
        )


    return render_template(
        "progressions/formulaire.html",
        form=form,
        progression=None
    )


# ==========================
# MODIFICATION
# ==========================

@bp_progressions.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):

    progression = db.session.get(Progression, id)
    if not progression:
        try:
            raise ProgressionIntrouvableException(id)
        except ProgressionIntrouvableException as exc:
            flash(str(exc), "danger")
            return redirect(url_for("progressions.lister"))

    form = ProgressionForm(obj=progression)


    form.talibe_matricule.choices = [
        (
            t.matricule,
            f"{t.prenom} {t.nom}"
        )
        for t in Talibe.query.all()
    ]


    if form.validate_on_submit():

        progression.sourate = form.sourate.data
        progression.nombre_versets = form.nombre_versets.data
        progression.date_evaluation = form.date_evaluation.data
        progression.observations = form.observations.data
        progression.talibe_matricule = form.talibe_matricule.data


        db.session.commit()


        flash(
            "Progression modifiée",
            "success"
        )


        return redirect(
            url_for("progressions.lister")
        )


    return render_template(
        "progressions/formulaire.html",
        form=form,
        progression=progression
    )


# ==========================
# SUPPRESSION
# ==========================

@bp_progressions.route("/supprimer/<int:id>", methods=["POST"])
def supprimer(id):

    try:
        progression = db.session.get(Progression, id)
        if not progression:
            raise ProgressionIntrouvableException(id)

        db.session.delete(progression)
        db.session.commit()

        flash(
            "Progression supprimée",
            "success"
        )
    except ProgressionIntrouvableException as exc:
        flash(str(exc), "danger")

    return redirect(
        url_for("progressions.lister")
    )


# ==========================
# EXPORT CSV
# ==========================

@bp_progressions.route("/export/csv")
def export_csv():

    recherche = request.args.get("q")
    talibe_matricule = request.args.get("talibe", "").strip()

    progressions = Progression.query.join(Talibe)

    if recherche:
        progressions = progressions.filter(
            db.or_(
                Progression.sourate.ilike(f"%{recherche}%"),
                Talibe.prenom.ilike(f"%{recherche}%"),
                Talibe.nom.ilike(f"%{recherche}%")
            )
        )

    if talibe_matricule:
        progressions = progressions.filter(Progression.talibe_matricule == talibe_matricule)

    progressions = progressions.all()

    return exporter_progressions_csv(progressions)