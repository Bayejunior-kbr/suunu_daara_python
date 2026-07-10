class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:passer@localhost:5432/daara"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "daara-secret-key"