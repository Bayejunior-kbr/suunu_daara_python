# app/models/user.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extension import db
from app.models.base import BaseModel

class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)  # <-- AJOUTE CETTE LIGNE
    nom_utilisateur = db.Column(db.String(50), unique=True, nullable=False)
    mot_de_passe_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="admin")

    def set_password(self, mot_de_passe):
        self.mot_de_passe_hash = generate_password_hash(mot_de_passe)

    def check_password(self, mot_de_passe):
        return check_password_hash(self.mot_de_passe_hash, mot_de_passe)