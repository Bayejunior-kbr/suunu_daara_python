# app/forms/auth_form.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nom_utilisateur = StringField("Nom d'utilisateur", validators=[DataRequired()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")