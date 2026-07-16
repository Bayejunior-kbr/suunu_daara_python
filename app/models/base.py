from datetime import datetime, timezone
from app.extension import db


def _maintenant():
    return datetime.now(timezone.utc)

class BaseModel(db.Model):
    __abstract__ = True

    cree_le = db.Column(db.DateTime, default=_maintenant, nullable=False)
    maj_le = db.Column( db.DateTime, default=_maintenant, onupdate=_maintenant, nullable=False)
