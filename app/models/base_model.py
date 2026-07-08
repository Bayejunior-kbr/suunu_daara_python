from email.policy import default

from app.extension import db
from datetime import datetime

class BaseModel(db.Model):
    __abstract__=True  # Cette classe ne crée PAS de table dans la BDD, elle sert juste de "modèle parent"

    id=db.Column(db.Integer, primary_key=True)
    cree_le=db.Column(db.DateTime, default=datetime.utcnow)
    mise_j=db.Column(db.DateTime,default=datetime.utcnow)

    #cette model va etre heriter pas tout les classe