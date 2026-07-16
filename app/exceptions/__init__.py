class DaaraException(RuntimeError):
    """Racine commune de toutes les exceptions métier du projet."""
    pass


class SuppressionImpossibleException(DaaraException):
    """Levée quand une suppression violerait une contrainte de relation"""
    def __init__(self, message: str):
        super().__init__(message)


class MaitreIntrouvableException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Aucun maître trouvé pour le matricule : {matricule}")


class MaitreDejaExistantException(DaaraException):
    def __init__(self, matricule: str):
        super().__init__(f"Un maître avec le matricule « {matricule} » existe déjà")


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
