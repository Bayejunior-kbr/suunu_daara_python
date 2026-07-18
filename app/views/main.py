"""
Blueprint principal : page d'accueil du projet Daara.
"""
from flask import Blueprint, render_template
from flask_login import login_required

bp_main = Blueprint("main", __name__)

@bp_main.route("/")
@login_required
def accueil():
    return render_template("index.html")