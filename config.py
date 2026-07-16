class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Bayejunior31@localhost:5432/suunu_daara"
    SECRET_KEY = "daara-secret-key" #cle secrete ki permet a flask de securiser les session et cookies(lee sert a chiffrer les donnees)