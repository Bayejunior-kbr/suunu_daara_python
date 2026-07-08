from sqlalchemy.orm import backref
from app.extension import db
from app.models.base_model import BaseModel

class Talibe(BaseModel):
    __tablename__="talibes" # le nom de la table en base de donnes

    nom=db.Column(db.String(100),nullable=False)
    prenom=db.Column(db.String(100),nullable=False)
    date_naissance=db.Column(db.Date,nullable=False)
    telephone_tuteur=db.Column(db.String(20),nullable=False)
    adresse=db.Column(db.String(200),nullable=False)

    #classe c'est la models classe.py

    classe_id=db.Column(db.Integer,db.ForeignKey("classes.id"),nullable=False)
    classe=db.relationship("Classe",backref="talibes")

    def __repr__(self):
        return f"(Talibes {self.prenom} {self.nom})"

    #nullable=False  ->> la valeur ne peut pas etre null