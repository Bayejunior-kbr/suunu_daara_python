class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:motdepasse@localhost:5432/suunu_daara"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "daara-secret-key"