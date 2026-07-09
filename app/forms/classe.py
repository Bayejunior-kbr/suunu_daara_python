# app/forms/classe.py
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


class ClasseForm(FlaskForm):
    code = StringField(
        'Code',
        validators=[DataRequired(), Length(max=50)]
    )
    libelle = StringField(
        'Libellé',
        validators=[DataRequired(), Length(max=150)]
    )
    niveau = StringField(
        'Niveau',
        validators=[Length(max=50)]
    )
    maitre_matricule = SelectField(
        'Maître',
        validators=[DataRequired()]
        # choices alimenté dans la vue (Maitre.query)
    )
    submit = SubmitField('Enregistrer')