"""
Hiérarchie d'exceptions métier du projet Daara.

Toutes héritent de DaaraException. Chaque entité aura ses propres
exceptions "introuvable" / "déjà existant". Ici : celles du module Maitre,
plus la base commune SuppressionImpossibleException réutilisable par tous.

Règle du projet : ces exceptions sont levées ET capturées dans la couche
views (jamais dans les templates).
"""


class DaaraException(RuntimeError):
    """Racine commune de toutes les exceptions métier du projet."""
    pass


class SuppressionImpossibleException(DaaraException):
    """Levée quand une suppression violerait une contrainte de relation
    (ex : maître encadrant encore des classes)."""
    def __init__(self, message: str):
        super().__init__(message)


# --- Exceptions propres à l'entité Maitre --------------------------------

class MaitreIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun maître trouvé pour le matricule : {matricule}")


class MaitreDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un maître avec le matricule « {matricule} » existe déjà")


# --- Autres exceptions du projet (stubs pour les coéquipiers) ------------
# À déplacer dans leurs propres fichiers si l'équipe préfère un fichier
# par entité (ex: exceptions/classe.py) ; sinon les ajouter ici.

class ClasseIntrouvableException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Aucune classe trouvée pour le code : {code}")


class ClasseDejaExistanteException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Une classe avec le code « {code} » existe déjà")


class TalibeIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun talibé pour le matricule : {matricule}")


class TalibeDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un talibé avec le matricule « {matricule} » existe déjà")


class ProgressionIntrouvableException(DaaraException):
    def __init__(self, progression_id):
        super().__init__(f"Aucune progression trouvée pour l'id : {progression_id}")


class ProgressionInvalideException(DaaraException):
    def __init__(self, message: str = "Progression invalide"):
        super().__init__(message)
