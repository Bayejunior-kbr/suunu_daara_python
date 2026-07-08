from app.extension import db
from app.models.base_model import BaseModel

#cree unique ma pour des teste

class Classe(BaseModel):
    __tablename__="classes"

    nom=db.Column(db.String(100),nullable=False)

    def __repr__(self):
        return f"'classes {self.nom}"
