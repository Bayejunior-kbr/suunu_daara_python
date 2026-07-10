"""
Application factory du projet Daara.
"""
import os

from flask import Flask

from config import config_by_name
from app.extension import db, migrate, csrf


def create_app(config_name: str | None = None) -> Flask:
    """Construit et retourne l'application Flask configurée."""
    app = Flask(__name__)

    config_name = config_name or os.getenv("FLASK_CONFIG", "dev")
    app.config.from_object(config_by_name[config_name])

    # --- Extensions ---
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # --- Modèles (nécessaire pour que Flask-Migrate les détecte) ---
    from app import models  # noqa: F401

    # --- Blueprints ---
    from app.views.main import bp_main
    from app.views.maitre import bp_maitres

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_maitres)
    # Blueprints à ajouter par les coéquipiers :
    # from app.views.classe import bp_classes
    # from app.views.talibe import bp_talibes
    # from app.views.progression import bp_progressions
    # app.register_blueprint(bp_classes)
    # app.register_blueprint(bp_talibes)
    # app.register_blueprint(bp_progressions)

    # --- Commande CLI utilitaire : flask seed ---
    from app.cli import register_cli
    register_cli(app)

    return app
