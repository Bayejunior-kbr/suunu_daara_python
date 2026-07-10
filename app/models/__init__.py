"""
Ce fichier importe tous les modèles pour que SQLAlchemy/Alembic les
détecte lors des migrations (flask db migrate). Chaque nouveau modèle
ajouté par un membre de l'équipe doit être importé ici.
"""
from app.models.base import BaseModel
from app.models.maitre import Maitre
from app.models.classe import Classe
# from app.models.talibe import Talibe          # à ajouter par le coéquipier concerné
# from app.models.progression import Progression  # à ajouter par le coéquipier concerné

__all__ = ["BaseModel", "Maitre", "Classe"]
