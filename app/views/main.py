"""
Blueprint principal : page d'accueil du projet Daara.
"""
from flask import Blueprint, render_template

bp_main = Blueprint("main", __name__)


@bp_main.route("/")
def accueil():
    return render_template("index.html")
