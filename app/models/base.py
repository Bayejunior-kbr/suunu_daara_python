"""
Classe de base abstraite héritée par toutes les entités du projet.
Aucune table n'est créée pour BaseModel (__abstract__ = True) : elle
fournit uniquement des colonnes communes de traçabilité.
"""
from datetime import datetime, timezone
from app.extension import db


def _maintenant():
    return datetime.now(timezone.utc)


class BaseModel(db.Model):
    __abstract__ = True

    cree_le = db.Column(db.DateTime, default=_maintenant, nullable=False)
    maj_le = db.Column(
        db.DateTime, default=_maintenant, onupdate=_maintenant, nullable=False
    )
