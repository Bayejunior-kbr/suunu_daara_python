from flask_wtf import FlaskForm
from wtforms.validators import Length, DataRequired, Optional
from wtforms import StringField, DateField, SubmitField, SelectField


class TalibeForm(FlaskForm):

    nom=StringField( "Nom", validators=[DataRequired(message="Le nom est obligatoir"),Length(max=100)])
    prenom=StringField("Prenom",validators=[DataRequired(message="Le prenom est obligatoire"), Length(max=100)])
    date_naissance=DateField("Date de naissance", validators=[Optional()],format="%Y-%m-%d")
    telephone_tuteur=StringField("Telephone du tuteur",validators=[Optional(),Length(max=20)])
    adresse=StringField("Adresse",validators=[Optional(),Length(max=200)])
    classe_id=SelectField("classe",coerce=int,validators=[DataRequired(message="Veuillez choisir une classe")])
    submit=SubmitField("Enregistre")

    #StringField, DateField, SelectField --> corespond aux champ de notre modele(nom,prenom,date_naissance,classe_id...)
    #validator-->empeche l'utilisateur de soumetre le formulaire si le champ est vide
    #Optional() → le champ n'est pas obligatoire
    #coerce=int --> convertit la valeur choisie en nombre entier(car en base c'est in id numerique)


