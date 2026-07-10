"""
STUB MINIMAL — module Classe.

⚠️ CE FICHIER N'EST PAS DE MA RESPONSABILITÉ (je m'occupe du module Maitre).
Il existe ici uniquement pour que :
  1) la relation Maitre <-> Classe fonctionne (ForeignKey obligatoire) ;
  2) mes tests et la vérification "suppression interdite si le maître a des
     classes" soient testables dès maintenant.

Le membre de l'équipe en charge du module Classe doit :
  - reprendre ce fichier et le compléter (niveau, validations, etc.) ;
  - créer forms/classe.py, views/classe.py, templates/classes/* ;
  - créer les exceptions ClasseIntrouvableException / ClasseDejaExistanteException.

Ne pas dupliquer ce fichier : un seul app/models/classe.py doit exister
dans le projet final assemblé par l'équipe.
"""
from app.extension import db
from app.models.base import BaseModel


class Classe(BaseModel):
    __tablename__ = "classes"

    code = db.Column(db.String(50), primary_key=True)
    libelle = db.Column(db.String(150), nullable=False)
    niveau = db.Column(db.String(50))

    maitre_matricule = db.Column(
        db.String(50), db.ForeignKey("maitres.matricule"), nullable=False
    )
    maitre = db.relationship("Maitre", back_populates="classes")

    def __repr__(self) -> str:
        return f"<Classe {self.code} - {self.libelle}>"
