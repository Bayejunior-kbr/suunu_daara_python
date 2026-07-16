from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, Optional
from wtforms import StringField, DateField, SubmitField, SelectField


class TalibeForm(FlaskForm):

    matricule = StringField(
        "Matricule",
        validators=[DataRequired(message="Le matricule est obligatoire"), Length(max=50)],
    )
    nom = StringField("Nom", validators=[DataRequired(message="Le nom est obligatoir"), Length(max=100)])
    prenom = StringField("Prenom", validators=[DataRequired(message="Le prenom est obligatoire"), Length(max=100)])
    date_naissance = DateField("Date de naissance", validators=[Optional()], format="%Y-%m-%d")
    nom_tuteur = StringField("Nom du tuteur", validators=[Optional(), Length(max=200)])
    telephone_tuteur = StringField("Telephone du tuteur", validators=[Optional(), Length(max=20)])
    adresse = StringField("Adresse", validators=[Optional(), Length(max=200)])


    classe_code = SelectField("classe", coerce=str, validators=[DataRequired(message="Veuillez choisir une classe")])
    submit = SubmitField("Enregistrer")

    # StringField, DateField, SelectField --> corespond aux champ de notre modele(nom,prenom,date_naissance,classe_code...)
    # validator-->empeche l'utilisateur de soumetre le formulaire si le champ est vide
    # Optional() → le champ n'est pas obligatoire
