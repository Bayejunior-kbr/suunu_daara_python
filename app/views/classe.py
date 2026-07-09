# app/views/classe.py
from flask import Blueprint, render_template, request, redirect, url_for, flash

from app.extension import db
from app.models.classe import Classe
from app.models.maitre import Maitre
from app.forms.classe import ClasseForm
from app.exceptions import (
    ClasseIntrouvableException,
    ClasseDejaExistanteException,
    SuppressionImpossibleException,
)

bp_classes = Blueprint('classes', __name__, url_prefix='/classes')


@bp_classes.route('/')
def lister():
    q = request.args.get('q', '').strip()

    query = Classe.query
    if q:
        query = query.filter(
            Classe.libelle.ilike(f'%{q}%') | Classe.niveau.ilike(f'%{q}%')
        )

    classes = query.order_by(Classe.libelle).all()
    return render_template('classes/liste.html', classes=classes, q=q)

@bp_classes.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    form = ClasseForm()
    form.maitre_matricule.choices = [
        (m.matricule, f"{m.prenom} {m.nom}") for m in Maitre.query.order_by(Maitre.nom).all()
    ]

    if form.validate_on_submit():
        if db.session.get(Classe, form.code.data):
            raise ClasseDejaExistanteException(form.code.data)

        classe = Classe(
            code=form.code.data,
            libelle=form.libelle.data,
            niveau=form.niveau.data,
            maitre_matricule=form.maitre_matricule.data
        )
        db.session.add(classe)
        db.session.commit()
        flash('Classe ajoutée.', 'success')
        return redirect(url_for('classes.lister'))

    return render_template('classes/formulaire.html', form=form, classe=None)



@bp_classes.route('/<code>/modifier', methods=['GET', 'POST'])
def modifier(code):
    classe = db.session.get(Classe, code)
    if not classe:
        raise ClasseIntrouvableException(code)

    form = ClasseForm(obj=classe)
    form.maitre_matricule.choices = [
        (m.matricule, f"{m.prenom} {m.nom}") for m in Maitre.query.order_by(Maitre.nom).all()
    ]

    if form.validate_on_submit():

        classe.libelle = form.libelle.data
        classe.niveau = form.niveau.data
        classe.maitre_matricule = form.maitre_matricule.data
        db.session.commit()
        flash('Classe modifiée.', 'success')
        return redirect(url_for('classes.lister'))

    return render_template('classes/formulaire.html', form=form, classe=classe)


@bp_classes.route('/<code>/supprimer', methods=['POST'])
def supprimer(code):
    classe = db.session.get(Classe, code)
    if not classe:
        raise ClasseIntrouvableException(code)

    from app.models.talibe import Talibe

    nb_talibes = Talibe.query.filter_by(classe_code=code).count()
    if nb_talibes > 0:
        raise SuppressionImpossibleException(
            f"Impossible de supprimer la classe {code} : elle contient {nb_talibes} talibé(s)."
        )

    db.session.delete(classe)
    db.session.commit()
    flash('Classe supprimée.', 'success')
    return redirect(url_for('classes.lister'))

from app.utils.csv_exporter import exporter_csv


@bp_classes.route('/export')
def exporter():
    q = request.args.get('q', '').strip()

    query = Classe.query
    if q:
        query = query.filter(
            Classe.libelle.ilike(f'%{q}%') | Classe.niveau.ilike(f'%{q}%')
        )

    classes = query.order_by(Classe.libelle).all()

    entetes = ['code', 'libelle', 'niveau', 'maitre_matricule']
    lignes = [
        [c.code, c.libelle, c.niveau, c.maitre_matricule]
        for c in classes
    ]

    return exporter_csv('classes.csv', entetes, lignes)