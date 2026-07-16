from flask import Flask
from app.extension import db, migrate,csrf
from app.exceptions import DaaraException

def create_app():
    app=Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)
    csrf.init_app(app)

    from app.views.main import bp_main
    from app.views.maitre import bp_maitres
    from app.views.classe import bp_classes
    from app.views.talibe import talibes_bp
    from app.views.progression import bp_progressions

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_maitres)
    app.register_blueprint(bp_classes)
    app.register_blueprint(talibes_bp)
    app.register_blueprint(bp_progressions)

    @app.errorhandler(DaaraException)
    def gerer_exception_daara(erreur):
        from flask import flash, redirect, request
        flash(str(erreur), "danger")
        return redirect(request.referrer or "/")
    return app