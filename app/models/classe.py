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

    maitre = db.relationship("Maitre", back_populates="classes") #permet de mettre en relation deux models sa veut dire dans la modele classes y'aun attribut nomme maitre

    def __repr__(self):
        return f"<Classe {self.code} - {self.libelle}>"