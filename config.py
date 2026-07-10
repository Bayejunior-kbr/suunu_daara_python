"""
Configuration multi-environnements de l'application Daara.

Chaque classe représente un environnement (dev, test, prod). Les secrets
(mot de passe BDD, SECRET_KEY) sont lus depuis les variables d'environnement
(fichier .env, non versionné) — jamais codés en dur dans le dépôt Git.
"""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Configuration commune à tous les environnements."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-changez-moi")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Active la protection CSRF sur tous les formulaires (Flask-WTF)
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(BaseConfig):
    """Environnement de développement local."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DEV_DATABASE_URL",
        "postgresql+psycopg2://daara_user:daara_pass@localhost:5432/daara_dev",
    )


class TestingConfig(BaseConfig):
    """Environnement de tests automatisés (pytest)."""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False  # simplifie les tests de formulaires
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql+psycopg2://daara_user:daara_pass@localhost:5432/daara_test",
    )


class ProductionConfig(BaseConfig):
    """Environnement de production."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")


# Dictionnaire utilisé par create_app() pour choisir la configuration
config_by_name = {
    "dev": DevelopmentConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "test": TestingConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}
