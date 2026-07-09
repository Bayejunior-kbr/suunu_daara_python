
class DaaraException(RuntimeError):
    pass


class ClasseIntrouvableException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Aucune classe pour le code : {code}")


class ClasseDejaExistanteException(DaaraException):
    def __init__(self, code: str):
        super().__init__(f"Une classe existe déjà avec le code : {code}")


class SuppressionImpossibleException(DaaraException):
    def __init__(self, message: str):
        super().__init__(message)