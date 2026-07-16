
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class MaitreForm(FlaskForm):
    matricule = StringField(
        "Matricule",
        validators=[DataRequired(message="Le matricule est obligatoire."), Length(max=50)],
    )
    prenom = StringField(
        "Prénom",
        validators=[DataRequired(message="Le prénom est obligatoire."), Length(max=100)],
    )
    nom = StringField(
        "Nom",
        validators=[DataRequired(message="Le nom est obligatoire."), Length(max=100)],
    )
    telephone = StringField(
        "Téléphone",
        validators=[
            Optional(),
            Length(max=20),
            Regexp(r"^[0-9+\s\-]*$", message="Numéro de téléphone invalide."),
        ],
    )
    submit = SubmitField("Enregistrer")
