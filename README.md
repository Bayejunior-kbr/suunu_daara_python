# 📚 Suunu Daara — Module Talibé

Ce README documente **le module Talibé** du projet `suunu_daara_python`, développé dans le cadre du projet de groupe L2GL (application de gestion de Daara en Flask, architecture MVC/Blueprint).

Responsable du module : **Baye Dame Koba** (Chef de groupe)

---

## 🎯 À quoi sert ce module ?

Le module Talibé permet de gérer les élèves (talibés) d'un Daara :
- Ajouter un talibé
- Modifier ses informations
- Le supprimer
- Lister tous les talibés
- Rechercher un talibé par nom
- Exporter la liste en fichier CSV

Chaque talibé est rattaché à une **Classe** (relation gérée par un autre membre de l'équipe).

---

## 🛠️ Stack technique — ce qu'on a installé et pourquoi

| Outil / Librairie | Rôle | Pourquoi on en a besoin |
|---|---|---|
| **Python** (venv) | Langage de programmation | Base de tout le projet |
| **Flask** | Micro-framework web | Gère les routes (URLs), les requêtes HTTP, sert les pages |
| **Flask-SQLAlchemy** | ORM (Object-Relational Mapping) | Permet d'écrire des modèles Python (`class Talibe`) au lieu d'écrire du SQL à la main |
| **Flask-Migrate** | Gestion des migrations de base de données | Suit l'historique des changements de structure de la BDD (ajout de colonnes, tables...) sans perdre les données existantes |
| **Flask-WTF** | Gestion des formulaires + protection CSRF | Valide les données saisies par l'utilisateur (champs obligatoires, longueur max, etc.) et sécurise les formulaires |
| **psycopg2-binary** | Connecteur PostgreSQL pour Python | Fait le pont entre SQLAlchemy et la vraie base de données PostgreSQL (sans lui, Python ne sait pas parler à PostgreSQL) |
| **PostgreSQL** | Système de gestion de base de données | Stocke réellement toutes les données (talibés, classes...) |
| **Bootstrap 5** (CDN) | Framework CSS | Donne un style visuel propre aux pages sans écrire tout le CSS à la main |

### Installer ces dépendances

```bash
pip install flask flask-sqlalchemy flask-migrate flask-wtf psycopg2-binary
```

Ou, si `requirements.txt` est à jour :
```bash
pip install -r requirements.txt
```

⚠️ Sur Windows, toujours préférer `psycopg2-binary` à `psycopg2` (évite d'avoir à compiler du code C).

---

## 📁 Structure des fichiers du module Talibé

```
app/
├── models/
│   ├── base_model.py      → modèle parent abstrait, partagé par tous (id, cree_le, mise_j)
│   ├── talibe.py           → le modèle Talibe (les colonnes de la table "talibes")
│   └── classe.py           → ⚠️ TEMPORAIRE, à remplacer par le vrai fichier du collègue
│
├── forms/
│   └── talibe.py           → le formulaire Flask-WTF (validation des champs)
│
├── views/
│   └── talibe.py           → le Blueprint : toutes les routes (/talibes/...)
│
└── templates/
    ├── base.html            → ⚠️ TEMPORAIRE, structure HTML commune (à remplacer par la vraie UI)
    └── talibes/
        ├── liste.html        → page listant tous les talibés
        └── formulaire.html   → formulaire réutilisé pour Ajouter ET Modifier
```

### 🔴 Fichiers temporaires — à ne pas fusionner tels quels sur `develop`/`main`

- **`app/models/classe.py`** : version minimale créée uniquement pour pouvoir tester Talibé sans attendre le vrai modèle Classe. À remplacer dès que le collègue responsable de Classe pousse son fichier définitif (le nom de table `classes` doit rester identique).
- **`app/templates/base.html`** : structure HTML minimale. À remplacer par la vraie intégration UI/Bootstrap commune à toute l'équipe.

---

## 🔌 Comment le module est branché à l'application

Dans `app/__init__.py`, le Blueprint est enregistré comme ceci :

```python
from app.views.talibe import talibe_bp
app.register_blueprint(talibe_bp)
```

Toutes les routes du module sont donc préfixées par `/talibes/` :

| Méthode | URL | Action |
|---|---|---|
| GET | `/talibes/` | Liste tous les talibés |
| GET/POST | `/talibes/ajouter` | Ajouter un talibé |
| GET/POST | `/talibes/modifier/<id>` | Modifier un talibé existant |
| POST | `/talibes/supprimer/<id>` | Supprimer un talibé |
| GET | `/talibes/rechercher?q=...` | Rechercher par nom |
| GET | `/talibes/export` | Télécharger la liste en CSV |

---

## 🗄️ Base de données — mise en place

**1. Créer/vérifier la base PostgreSQL** `suunu_daara` (config dans `config.py`)

**2. Générer et appliquer les migrations**
```bash
flask db init        # une seule fois pour tout le projet
flask db migrate -m "ajout table talibes"
flask db upgrade
```

- `migrate` = prépare le script de changement (compare les modèles Python à l'état actuel de la BDD)
- `upgrade` = applique réellement le changement en base

**3. (Optionnel, pour tester) Ajouter des classes de test**

Via `flask shell` :
```python
from app.extension import db
from app.models.classe import Classe

db.session.add(Classe(nom="CI"))
db.session.add(Classe(nom="CP"))
db.session.commit()
```

---

## ▶️ Lancer le serveur

**Recommandé pendant le développement** (rechargement automatique + erreurs détaillées) :
```bash
flask run --debug
```

Ou, si `run.py` contient `app.run(debug=True)` :
```bash
python run.py
```

Puis ouvrir : **http://127.0.0.1:5000/talibes/**

---

## 🐛 Bugs rencontrés et corrigés pendant le développement

Petit historique utile pour l'équipe (et pour se souvenir des pièges classiques) :

| Erreur | Cause | Correction |
|---|---|---|
| `ModuleNotFoundError: No module named 'psycopg2'` | Librairie de connexion PostgreSQL manquante | `pip install psycopg2-binary` |
| `TypeError: column() got an unexpected keyword argument 'default'` | `db.column` (minuscule) au lieu de `db.Column` (majuscule) | Corriger la casse |
| `UnicodeDecodeError` lors de la connexion PostgreSQL | Encodage Windows, souvent lié au mot de passe | `$env:PGCLIENTENCODING="UTF8"` ou mot de passe simplifié |
| Page vide malgré un rendu réussi (200) | `{% block content %}{% endblock %}` manquant dans `base.html` | Ajouter le bloc dans le template parent |
| `BuildError: Could not build url for endpoint` | Nom de fonction Python ≠ nom utilisé dans `url_for()` | Rendre les noms identiques partout |
| `TypeError: unexpected keyword argument 'validator'` | `validator=` (singulier) au lieu de `validators=` (pluriel) | Corriger dans `forms/talibe.py` |
| Menu déroulant "classe" vide | `form.classe_id.choix = ...` au lieu de `.choices = ...` | Corriger le nom d'attribut (piège : Python ne signale pas l'erreur car `choix` devient juste un nouvel attribut inutile) |
| `TemplateNotFound: talibes/formlaire.html` | Faute de frappe dans le nom du fichier appelé | `formulaire.html` (avec le "u") |

---

## ✅ État actuel du module

- [x] Modèle Talibe avec relation vers Classe (par nom de table, pas d'import direct → évite le blocage inter-équipe)
- [x] Formulaire avec validations
- [x] CRUD complet (Créer, Lire, Modifier, Supprimer)
- [x] Recherche par nom
- [x] Export CSV
- [x] Templates avec Bootstrap (mise en page centrée)

## 🔜 À faire avant la fusion sur `develop`

- [ ] Remplacer `models/classe.py` temporaire par le vrai fichier du collègue
- [ ] Remplacer `templates/base.html` temporaire par la vraie base UI commune
- [ ] Vérifier la cascade de suppression avec le module Progression
- [ ] Tests d'intégration avec les 3 autres modules (Maître, Classe, Progression)