from flask import Flask
from app.extension import db, migrate


def create_app():

    app = Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)

    # Chargement des modèles
    from app.models.maitre import Maitre
    from app.models.classe import Classe
    from app.models.talibe import Talibe
    from app.models.progression import Progression

    # Blueprints
    from app.views.progression import bp_progressions

    app.register_blueprint(bp_progressions)

    return app