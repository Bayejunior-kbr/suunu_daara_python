from app.extension import db
from app.models.base import BaseModel


class Talibe(BaseModel):
    __tablename__ = "talibes"  # le nom de la table en base de donnees


    matricule = db.Column(db.String(50), primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=True)
    nom_tuteur = db.Column(db.String(200))
    telephone_tuteur = db.Column(db.String(20))
    adresse = db.Column(db.String(200))  # champ en plus, utile pour la fiche talibé

    # classe c'est le modele classe.py
    classe_code = db.Column(db.String(50), db.ForeignKey("classes.code"), nullable=False)
    classe = db.relationship("Classe", backref="talibes")

    # un talibe peut avoir plusieurs progressions
    # cascade="all, delete-orphan" -> supprimer un talibe supprime aussi ses progressions
    progressions = db.relationship(
        "Progression", back_populates="talibe", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Talibe {self.matricule} - {self.prenom} {self.nom}>"

    # nullable=False  ->> la valeur ne peut pas etre null
