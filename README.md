# Module Maître — Projet « Gestion d'une Daara »

Ce dépôt contient **ma partie du projet d'équipe** : le module métier
**Maitre**, complet et fonctionnel (modèles, formulaires, Blueprint,
templates, exceptions, export CSV, tests automatisés), plus le **socle
commun minimal** nécessaire pour que l'application tourne seule le
temps de la présentation, avant fusion avec le travail des coéquipiers
(Classe, Talibé, Progression).

## 1. Ce qui est livré

| Couche | Fichier | Contenu |
|---|---|---|
| Modèle | `app/models/maitre.py` | Entité `Maitre` (matricule PK string, relation vers `Classe`) |
| Modèle (stub) | `app/models/classe.py` | ⚠️ Version minimale, juste pour la FK — **à fusionner avec le coéquipier en charge de Classe** |
| Formulaire | `app/forms/maitre.py` | `MaitreForm` (WTForms + validations) |
| Contrôleur | `app/views/maitre.py` | Blueprint `maitres` : lister, rechercher, créer, modifier, supprimer, exporter CSV |
| Exceptions | `app/exceptions/__init__.py` | `MaitreIntrouvableException`, `MaitreDejaExistantException`, `SuppressionImpossibleException` (+ stubs pour les autres entités) |
| Vues | `app/templates/maitres/liste.html`, `formulaire.html` | Templates Jinja2 |
| Utilitaire | `app/utils/csv_exporter.py` | Export CSV générique, réutilisable par toute l'équipe |
| Socle | `app/__init__.py`, `config.py`, `app/extension.py`, `run.py` | App factory, config multi-environnements, extensions |
| Tests | `tests/test_maitre.py` | 17 tests automatisés (CRUD, recherche, CSV, règles métier) |

**Règles métier implémentées** (conformes à l'énoncé) :
- matricule unique → `MaitreDejaExistantException` si doublon à la création ;
- suppression **interdite** si le maître encadre au moins une classe → `SuppressionImpossibleException` ;
- recherche par nom / prénom / matricule ;
- export CSV qui respecte le filtre de recherche actif.

J'ai testé ce module de A à Z dans un environnement PostgreSQL réel :
migrations Alembic générées et appliquées, `flask seed`, serveur lancé,
et **les 17 tests passent**. Vous pouvez reproduire exactement les mêmes
étapes ci-dessous.

## 2. Installation (à faire une fois par machine)

### Prérequis
- Python 3.11+
- PostgreSQL installé et démarré

### Étapes

```bash
# 1. Se placer dans le dossier du projet, créer et activer le venv
python3 -m venv venv
source venv/bin/activate          # Windows : venv\Scripts\activate

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer les bases PostgreSQL (une seule fois, via psql ou pgAdmin)
psql -U postgres -c "CREATE USER daara_user WITH PASSWORD 'daara_pass';"
psql -U postgres -c "CREATE DATABASE daara_dev OWNER daara_user ENCODING 'UTF8';"
psql -U postgres -c "CREATE DATABASE daara_test OWNER daara_user ENCODING 'UTF8';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE daara_dev TO daara_user;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE daara_test TO daara_user;"

# 4. Copier le fichier d'environnement et l'adapter si besoin
cp .env.example .env
# (ouvrez .env et changez le mot de passe/utilisateur si différent chez vous)

# 5. Initialiser les migrations et créer les tables
export FLASK_APP=run:app          # Windows (PowerShell) : $env:FLASK_APP="run:app"
flask db init
flask db migrate -m "init: maitres et classes"
flask db upgrade

# 6. Insérer des données de démonstration
flask seed

# 7. Lancer l'application
flask run
```

Ouvrez ensuite **http://127.0.0.1:5000/maitres/** — vous devriez voir 3
maîtres de démo, dont un (`M001`) rattaché à une classe.

> Le dossier `migrations/` fourni contient déjà la structure Alembic ;
> si vous relancez `flask db init` sur une machine où `migrations/`
> existe déjà, supprimez d'abord ce dossier ou passez directement à
> `flask db migrate` puis `flask db upgrade`.

## 3. Lancer les tests automatisés

```bash
source venv/bin/activate
export FLASK_APP=run:app
python -m pytest tests/ -v
```

Résultat attendu : **17 passed**. Les tests couvrent :
- affichage de la liste (vide, puis remplie) ;
- recherche par nom (avec et sans résultat) ;
- création (succès, matricule dupliqué, champs manquants) ;
- modification (succès, matricule inexistant) ;
- suppression (succès, bloquée si classes rattachées, matricule inexistant) ;
- export CSV (contenu exact, respect du filtre) ;
- méthodes métier du modèle (`nom_complet`, `a_des_classes`).

Les tests utilisent la base `daara_test` (PostgreSQL), configurée via
`TestingConfig` dans `config.py` — conformément à l'énoncé qui impose
PostgreSQL partout, seule l'URI changeant selon l'environnement.

## 4. Démonstration manuelle pour la soutenance

Un scénario simple à montrer en direct :

1. `flask run` → aller sur `/maitres/`
2. Créer un maître (`+ Nouveau maître`) → vérifier qu'il apparaît dans la liste
3. Retenter avec le même matricule → message d'erreur "existe déjà"
4. Rechercher par nom → la liste se filtre
5. Modifier un maître → le matricule est bien en lecture seule
6. Essayer de supprimer `M001` (qui encadre `CL-DEB`) → suppression refusée avec message explicite
7. Supprimer un maître sans classe → suppression acceptée
8. Cliquer sur "Exporter CSV" → le fichier se télécharge avec les bonnes colonnes

## 5. Intégration avec l'équipe

Ce dépôt est **prêt à être fusionné** avec le travail des autres membres :

- `app/models/classe.py` est un **stub minimal** — la personne en
  charge du module Classe doit reprendre ce fichier, y ajouter les
  champs/validations manquants, et créer `forms/classe.py`,
  `views/classe.py`, `templates/classes/*`.
- Dans `app/__init__.py`, les imports/blueprints des autres modules
  (`classe`, `talibe`, `progression`) sont indiqués en commentaire —
  il suffit de les décommenter et de brancher les Blueprints de chacun.
- `app/exceptions/__init__.py` contient déjà des stubs pour
  `Classe`, `Talibe`, `Progression` — chacun peut les compléter ou les
  déplacer dans des fichiers séparés si l'équipe préfère.
- `app/utils/csv_exporter.py` est générique : toute l'équipe peut
  l'appeler depuis ses propres vues (`exporter_csv(nom, entetes, lignes)`).
- Une seule migration Alembic doit exister au final : quand tout le
  monde aura ses modèles, régénérez une migration commune propre
  (`flask db migrate`) plutôt que d'empiler plusieurs migrations
  partielles.

## 6. Structure du projet

```
daara/
├── run.py
├── config.py
├── requirements.txt
├── .env.example
├── app/
│   ├── __init__.py          # create_app()
│   ├── extension.py         # db, migrate, csrf
│   ├── cli.py                # flask seed
│   ├── models/
│   │   ├── base.py           # BaseModel (cree_le, maj_le)
│   │   ├── maitre.py          # ✅ mon module
│   │   └── classe.py          # stub minimal (coéquipier)
│   ├── forms/
│   │   └── maitre.py          # ✅ mon module
│   ├── views/
│   │   ├── main.py            # accueil
│   │   └── maitre.py           # ✅ mon module (Blueprint complet)
│   ├── exceptions/
│   │   └── __init__.py        # ✅ mes exceptions + stubs équipe
│   ├── utils/
│   │   └── csv_exporter.py    # ✅ utilitaire partagé
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   └── maitres/            # ✅ mon module
│   └── static/css/style.css
├── migrations/                # Alembic
└── tests/
    ├── conftest.py
    └── test_maitre.py          # ✅ 17 tests
```
