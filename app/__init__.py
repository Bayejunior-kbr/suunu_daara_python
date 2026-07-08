from flask import Flask
from app.extension import db, migrate

def create_app():
    app=Flask(__name__)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app,db)

    from app.views.talibe import talibes_bp
    app.register_blueprint(talibes_bp)

    return app