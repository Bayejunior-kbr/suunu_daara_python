"""
Instances des extensions Flask, créées ici pour éviter les imports circulaires.
Elles sont initialisées (liées à l'app) dans create_app().
"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
