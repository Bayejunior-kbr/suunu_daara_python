from app.extension import db
from datetime import datetime


class BaseModel(db.Model):

    __abstract__ = True

    cree_le = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    maj_le = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )