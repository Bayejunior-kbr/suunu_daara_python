# app/blueprints/auth/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms.auth_form import LoginForm
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(nom_utilisateur=form.nom_utilisateur.data).first()
        if user and user.check_password(form.mot_de_passe.data):
            login_user(user)
            flash("Connexion réussie.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("talibes.liste"))
        flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template("auth/login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.", "info")
    return redirect(url_for("auth.login"))