from app.extension import db
from app.models.base import BaseModel


class Maitre(BaseModel):
    __tablename__ = "maitres"

    # Clé saisie par l'utilisateur (pas d'auto-incrément)
    matricule = db.Column(db.String(50), primary_key=True)
    prenom = db.Column(db.String(100), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(20))

    # Relation 1-N : un maître encadre plusieurs classes.
    # La classe "Classe" définit la ForeignKey (classe.maitre_matricule).
    classes = db.relationship(
        "Classe",
        back_populates="maitre",
    )

    def nom_complet(self) -> str:
        """Nom affichable dans les listes et formulaires."""
        return f"{self.prenom} {self.nom}"

    def a_des_classes(self) -> bool:
        """Utilisé pour bloquer la suppression (règle métier)."""
        return len(self.classes) > 0

    def __repr__(self) -> str:
        return f"<Maitre {self.matricule} - {self.nom_complet()}>"
