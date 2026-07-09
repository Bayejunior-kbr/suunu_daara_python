# app/models/classe.py
from app.extension import db
from app.models.base import BaseModel


class Classe(BaseModel):
    __tablename__ = "classes"

    # Clé saisie par l'utilisateur (pas d'auto-incrément)
    code = db.Column(db.String(50), primary_key=True)
    libelle = db.Column(db.String(150), nullable=False)
    niveau = db.Column(db.String(50))

    # Clé étrangère obligatoire vers Maitre
    maitre_matricule = db.Column(
        db.String(50),
        db.ForeignKey("maitres.matricule"),
        nullable=False
    )

    # backref="classes" crée automatiquement maitre.classes
    # sans modifier le fichier maitre.py
    maitre = db.relationship("Maitre", backref="classes")

    def __repr__(self):
        return f"<Classe {self.code} - {self.libelle}>"