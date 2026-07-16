# Suunu Daara — Projet d'examen Flask (Rendu final fusionné)

Application de gestion d'une Daara (Maîtres, Classes, Talibés, Progressions),
développée en Flask / SQLAlchemy / Jinja2 selon l'architecture MVC imposée
par l'énoncé. Ce dépôt est le **résultat de la fusion des 4 branches de
l'équipe** en une seule application fonctionnelle.

## Répartition du travail (par module)

| Membre           | Module responsable | Fichiers principaux |
|------------------|--------------------|----------------------|
| Babacar Samb     | **Maitre**         | `models/maitre.py`, `forms/maitre.py`, `views/maitre.py` — a aussi posé le squelette commun (`app/__init__.py`, `config.py`, `extension.py`, `exceptions/__init__.py`, `cli.py`) |
| Mouhamed Sène     | **Classe**         | `models/classe.py`, `forms/classe.py`, `views/classe.py`, `templates/classes/*` |
| Baye Dame         | **Talibé**         | `models/talibe.py`, `forms/talibe.py`, `views/talibe.py`, `templates/talibes/*` |
| Astou Thiam       | **Progression**    | `models/progression.py`, `forms/progression.py`, `views/progression.py`, `templates/progressions/*`, `utils/csv_exporter.py` (fonction `exporter_progressions_csv`) |

Les commentaires personnels laissés par chacun dans son code ont été
conservés lors de la fusion.

## Ce qui a été ajusté pendant la fusion

Chaque branche avait été développée isolément (certains modèles utilisaient
des stubs temporaires en attendant le travail des coéquipiers). Pour obtenir
une application unique et cohérente, les ajustements suivants ont été faits :

- **`models/talibe.py`** : la version de travail de Baye Dame utilisait un
  `id` auto-incrémenté et une `classe_id` (Integer) le temps que le module
  Classe ne soit pas prêt. Le modèle final utilise désormais le `matricule`
  (String, saisi par l'utilisateur) comme clé primaire et `classe_code`
  comme clé étrangère vers `classes.code`, conformément à l'énoncé et pour
  rester compatible avec les modules Classe et Progression des coéquipiers.
  Les champs ajoutés par Baye Dame (`adresse`) et ses commentaires
  explicatifs ont été conservés.
- **`models/classe.py`** : la relation `Classe.maitre` utilisait un
  `backref="classes"`, ce qui entrait en conflit avec la relation
  `Maitre.classes` (déjà définie via `back_populates` dans le module de
  Babacar). Remplacé par `back_populates="classes"` des deux côtés.
- **Gestion des exceptions** : certaines vues (Classe, Talibé, Progression)
  levaient une exception métier sans la capturer localement, ce qui aurait
  provoqué une erreur 500. Un `try/except` a été ajouté dans chaque vue
  concernée (sur le modèle du module Maitre), conformément à la règle du
  projet : *les exceptions sont levées ET capturées dans la couche views*.
  Un gestionnaire d'erreur global (`app.errorhandler(DaaraException)`) a
  aussi été ajouté comme filet de sécurité supplémentaire.
- **Templates `progressions/*`** : il manquait `{% extends "base.html" %}`
  et les blocs `{% block content %}` — ajoutés sans changer la structure ni
  le contenu écrits par Astou.
- **Base commune (`base.html`)** : fusionnée à partir de la version
  Bootstrap 5 de Baye Dame (conforme à la stack imposée), complétée avec une
  navbar reliant les 4 modules.
- **`utils/csv_exporter.py`** : contient désormais la fonction générique
  `exporter_csv()` (Babacar, utilisée par Maitre/Classe/Talibé) **et** la
  fonction spécifique `exporter_progressions_csv()` (Astou), sans rien
  supprimer du travail de personne.
- **CSRF** : quelques formulaires de suppression n'envoyaient pas
  correctement le jeton CSRF (valeur affichée hors d'un `<input>`) — corrigé
  pour que les suppressions fonctionnent avec la protection CSRF activée
  globalement.

Toute la fusion a été testée de bout en bout (création, recherche,
modification, suppression avec contraintes, cascade, export CSV, doublons de
clé) avant livraison.

## Stack technique

Python 3.11+, Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, PostgreSQL
(psycopg2-binary), Bootstrap 5, python-dotenv.

## Structure du projet

```
suunu_daara_python/
├── run.py
├── config.py
├── requirements.txt
├── .env.example
└── app/
    ├── __init__.py          # create_app()
    ├── extension.py         # db, migrate, csrf
    ├── cli.py                # commande "flask seed"
    ├── models/                # base.py, maitre.py, classe.py, talibe.py, progression.py
    ├── forms/                 # un formulaire WTForms par entité
    ├── views/                 # un Blueprint par entité + main.py
    ├── exceptions/             # hiérarchie DaaraException
    ├── utils/csv_exporter.py
    ├── static/{css,js}
    └── templates/
        ├── base.html, index.html
        ├── maitres/, classes/, talibes/, progressions/
```

## Table des routes

| Entité | Lister | Ajouter | Modifier | Supprimer | Export CSV |
|---|---|---|---|---|---|
| Maitre | `GET /maitres/` | `GET/POST /maitres/nouveau` | `GET/POST /maitres/<matricule>/modifier` | `POST /maitres/<matricule>/supprimer` | `GET /maitres/export.csv` |
| Classe | `GET /classes/` | `GET/POST /classes/ajouter` | `GET/POST /classes/<code>/modifier` | `POST /classes/<code>/supprimer` | `GET /classes/export` |
| Talibé | `GET /talibes/` | `GET/POST /talibes/ajouter` | `GET/POST /talibes/<matricule>/modifier` | `POST /talibes/<matricule>/supprimer` | `GET /talibes/export.csv` |
| Progression | `GET /progressions/` | `GET/POST /progressions/nouveau` | `GET/POST /progressions/modifier/<id>` | `POST /progressions/supprimer/<id>` | `GET /progressions/export/csv` |

## Lancement

```bash
# 1. Environnement virtuel
python -m venv venv
source venv/bin/activate      # Windows : venv\Scripts\activate

# 2. Dépendances
pip install -r requirements.txt

# 3. Configuration
cp .env.example .env
# → adapter DEV_DATABASE_URL avec vos identifiants PostgreSQL

# 4. Base de données (créer la base "daara_dev" dans PostgreSQL au préalable)
flask db init
flask db migrate -m "init"
flask db upgrade

# 5. (optionnel) données de démonstration
flask seed

# 6. Lancer l'application
flask run
```

L'application démarre sur http://127.0.0.1:5000/

## Règles métier implémentées

- Matricules/codes uniques (Maitre, Classe, Talibé) → `XDejaExistantException`.
- Suppression d'un maître interdite s'il encadre encore des classes.
- Suppression d'une classe interdite si elle contient des talibés.
- Suppression d'un talibé → cascade sur ses progressions.
- `nombre_versets >= 0` et `sourate` obligatoire (validateurs WTForms).
- Recherche par nom/prénom/matricule/libellé, filtre Talibés par classe et
  filtre Progressions par talibé.
- Export CSV respectant le filtre affiché, sur chacune des 4 pages.
