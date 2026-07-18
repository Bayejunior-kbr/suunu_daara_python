from flask import Flask
from app.extension import db, migrate,csrf,login_manager
from app.exceptions import DaaraException
from app.cli import create_admin


def create_app():
    app=Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)
    csrf.init_app(app)

    # ...
    app.cli.add_command(create_admin)

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

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Merci de vous connecter pour accéder à cette page."

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # enregistrer le blueprint auth
    from app.views.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    return app