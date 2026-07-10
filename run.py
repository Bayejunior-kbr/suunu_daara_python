import os
from dotenv import load_dotenv

load_dotenv()  # charge le fichier .env avant la création de l'app

from app import create_app  # noqa: E402

app = create_app(os.getenv("FLASK_CONFIG", "dev"))

if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", True))
