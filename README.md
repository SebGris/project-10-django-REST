# 🌐 SoftDesk API - Projet 10 OpenClassrooms

## 📋 Présentation

**SoftDesk** est une API REST sécurisée développée avec Django REST Framework pour la gestion collaborative de projets avec système de tickets (issues) et commentaires.

### ✨ Fonctionnalités principales
- 🔐 **Authentification JWT** sécurisée avec refresh tokens
- 👥 **Gestion des contributeurs** par projet avec permissions granulaires
- 🎫 **Système de tickets (issues)** avec assignations et priorités
- 💬 **Commentaires** sur les issues avec historique complet
- 🛡️ **Sécurité RGPD** avec consentement et gestion des données
- ⚡ **Optimisations Green Code** pour performances et écologie

## 📚 Documentation complète

### 🚀 Guides de démarrage
- **[Installation et configuration](#-installation-et-lancement-rapide)** - Setup complet avec Poetry
- **[Guide de test avec Postman](docs/postman/postman-guide.md)** - Collection complète d'endpoints

## 🚀 Installation et lancement rapide

### Prérequis
- Python 3.12+
- Poetry (gestionnaire de dépendances)

### 1. Installation de Poetry

```bash
# Installer pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Redémarrer le terminal ou VS Code, puis :
pipx install poetry
poetry --version
```

### 2. Installation du projet

```bash
# Cloner le repository
git clone https://github.com/SebGris/project-10-django-REST.git
cd project-10-django-REST

# Installer les dépendances
poetry install

# Vérifier l'installation
poetry run python --version
poetry run python -c "import django; print(f'Django {django.get_version()}')"
```

### 3. Configuration de la base de données

```bash
# Créer les migrations
poetry run python manage.py makemigrations users
poetry run python manage.py makemigrations issues
poetry run python manage.py makemigrations

# Appliquer les migrations
poetry run python manage.py migrate
```

### 4. Créer un superutilisateur

```bash
# Méthode recommandée (script personnalisé)
poetry run python create_superuser.py

# Ou méthode Django standard
poetry run python manage.py createsuperuser
```

**Identifiants par défaut du script :**
- Username: `admin`
- Email: `admin@softdesk.local`
- Password: `SoftDesk2025!`

### 5. Lancer le serveur

```bash
poetry run python manage.py runserver
```

🎉 **L'API est accessible à :** http://127.0.0.1:8000/

## 🧪 Vérifier l'installation

### Tests de base
```bash
# Test de configuration Django
poetry run python manage.py check

# Test simple des modèles
poetry run python test_simple.py

# Tests complets
poetry run python run_tests_universal.py
```

### Interface d'administration
- URL : http://127.0.0.1:8000/admin/
- Connexion avec le superutilisateur créé

### Interface API
- URL : http://127.0.0.1:8000/api/
- Documentation interactive Django REST Framework

## 📋 Endpoints principaux

| Endpoint | Méthode | Description | Auth | Body Format |
|----------|---------|-------------|------|-------------|
| `/api/token/` | POST | Obtenir token JWT | Non | `{"username": "user", "password": "pass"}` |
| `/api/users/` | POST | Inscription | Non | `{"username": "user", "email": "...", "password": "..."}` |
| `/api/users/` | GET | Liste utilisateurs | Oui | - |
| `/api/projects/` | GET/POST | Projets | Oui | `{"name": "...", "description": "...", "type": "back-end"}` |
| `/api/projects/{id}/` | GET/PUT/DELETE | Détails projet | Oui | - |
| `/api/projects/{id}/add-contributor/` | POST | Ajouter contributeur | Oui | `{"username": "user"}` ou `{"user_id": 1}` |
| `/api/projects/{project_id}/issues/` | GET/POST | Issues du projet | Oui | `{"name": "...", "description": "...", "tag": "BUG", "assigned_to_id": 1}` |
| `/api/projects/{project_id}/issues/{issue_id}/comments/` | GET/POST | Commentaires d'une issue | Oui | `{"description": "..."}` |

### Valeurs autorisées pour les champs :
- **Project.type** : `"back-end"`, `"front-end"`, `"iOS"`, `"Android"`
- **Issue.priority** : `"LOW"`, `"MEDIUM"`, `"HIGH"`
- **Issue.tag** : `"BUG"`, `"FEATURE"`, `"TASK"`
- **Issue.status** : `"To Do"`, `"In Progress"`, `"Finished"`

## 🔐 Authentification JWT

### Obtenir un token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}'
```

### Utiliser le token
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/
```

## 🚨 Résolution des problèmes

### Erreurs courantes

**"No module named 'softdesk_support'"**
```bash
# Utiliser Poetry au lieu de Python directement
poetry run python manage.py check
```

**Erreurs de migration**
```bash
# Réinitialiser la base de données
del db.sqlite3
poetry run python manage.py migrate
```

**Problème d'encodage (Windows)**
```bash
# Utiliser le script universel
poetry run python run_tests_universal.py
```

### Diagnostic complet
```bash
poetry run python diagnose_project.py
```

## 📚 Documentation

- 🏗️ **[Architecture du projet](docs/architecture/architecture.md)** - Structure et principes de conception
- 🧪 **[Guide des tests](tests/README.md)** - Suite de tests et exécution
- 🌱 **[Green Code](docs/green-code/green-code-guide.md)** - Optimisations éco-responsables
- 📖 **[API Guide](docs/api/api-guide.md)** - Documentation complète des endpoints
- 🔒 **[RGPD](docs/security/rgpd-compliance.md)** - Conformité et protection des données

## 🛠️ Développement

### Structure du projet
```
project-10-django-REST/
├── manage.py                 # Gestionnaire Django
├── pyproject.toml           # Configuration Poetry
├── users/                   # App utilisateurs (auth, profils)
├── issues/                  # App projets (projects, issues, comments)
├── softdesk_support/        # Configuration Django
├── tests/                   # Suite de tests organisée
└── docs/                    # Documentation
```

### Commandes utiles
```bash
# Démarrer le serveur
poetry run python manage.py runserver

# Activer l’environnement virtuel
poetry env activate
# Ensuite, Poetry vous donne le chemin vers le script d'activation de l'environnement virtuel.
# Cette réponse est normale avec `poetry env activate` - elle vous indique où se trouve le script d'activation.

# Créer une migration
poetry run python manage.py makemigrations

# Appliquer les migrations
poetry run python manage.py migrate

# Tests
poetry run python run_tests_universal.py

# Linting et formatage avec Ruff
poetry run ruff check .           # Vérifier le code
poetry run ruff check . --fix     # Corriger automatiquement
poetry run ruff format .          # Formater le code
poetry run ruff check . --output-format=full  # Format détaillé
```

## 📄 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Django - Saving objects](https://docs.djangoproject.com/en/5.2/ref/models/instances/#saving-objects)
- [Django - Overriding model methods](https://docs.djangoproject.com/en/5.2/topics/db/models/#overriding-model-methods)
- [DRF ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [DRF Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [JWT Authentication in Django](https://code.tutsplus.com/how-to-authenticate-with-jwt-in-django--cms-30460t)

---

**Projet réalisé dans le cadre de la formation OpenClassrooms "Développeur d'application Python"**
