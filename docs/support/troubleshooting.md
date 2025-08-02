# 🔧 Dépannage SoftDesk - Guide de Résolution des Problèmes

[← Retour à la documentation](../README.md)

## 📋 Table des matières
- [Problèmes d'installation](#problèmes-dinstallation)
- [Erreurs d'encodage](#erreur-dencodage-unicode)
- [Erreurs de migration](#erreurs-de-migration-django)
- [Problèmes d'authentification](#problèmes-dauthentification)
- [Erreurs d'API](#erreurs-dapi)

## 🚨 Problèmes d'installation

### 1. ❌ Poetry non installé

**Symptômes :**
```
poetry : Le terme 'poetry' n'est pas reconnu comme nom d'applet, fonction, fichier de script ou programme exécutable.
```

**Solutions :**

```bash
# Installer Poetry (si non installé)
curl -sSL https://install.python-poetry.org | python3 -

# Ajouter Poetry au PATH
# Suivre les instructions affichées après l'installation
```

### 2. ❌ Erreur d'encodage Unicode (Windows)

**Symptômes :**
```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f680'
```

**Cause :**
Emojis dans les scripts incompatibles avec `cmd.exe` Windows.

**Solutions :**

```bash
# Solution A : Script universel (recommandé)
poetry run python run_tests_universal.py

# Solution B : Forcer l'encodage UTF-8
set PYTHONIOENCODING=utf-8
poetry run python run_all_tests.py

# Solution C : PowerShell
$env:PYTHONIOENCODING="utf-8"
poetry run python run_all_tests.py

# Solution D : Utiliser VS Code Terminal
# Le terminal intégré de VS Code gère mieux l'UTF-8
```

### 3. ❌ Erreurs de migration Django

**Symptômes :**
```
django.db.utils.OperationalError: no such table: users_user
InconsistentMigrationHistory
```

**Solution complète :**

```bash
# 1. Sauvegarder les données si nécessaire
poetry run python manage.py dumpdata > backup.json

# 2. Supprimer la base de données
del db.sqlite3  # Windows
rm db.sqlite3   # macOS/Linux

# 3. Supprimer les fichiers de migration
del users\migrations\*.py
del issues\migrations\*.py

# 4. Recréer les __init__.py
echo. > users\migrations\__init__.py
echo. > issues\migrations\__init__.py

# 5. Recréer les migrations dans le bon ordre
poetry run python manage.py makemigrations users
poetry run python manage.py makemigrations issues
poetry run python manage.py makemigrations

# 6. Appliquer les migrations
poetry run python manage.py migrate

# 7. Recréer le superutilisateur
poetry run python create_superuser.py
```

### 4. ❌ Serveur Django ne démarre pas

**Symptômes :**
```
Error: That port is already in use.
CommandError: "migrate" not found
```

**Solutions :**

```bash
# Port occupé
poetry run python manage.py runserver 8001

# Forcer l'arrêt du processus (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Vérifier la configuration
poetry run python manage.py check --deploy

# Migrations manquantes
poetry run python manage.py migrate
```

### 5. ❌ Tests API échouent

**Symptômes :**
```
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```

**Causes et solutions :**

```bash
# 1. Serveur Django non démarré
# Terminal 1:
poetry run python manage.py runserver

# Terminal 2:
poetry run python tests/api/test_basic_api.py

# 2. Mauvaise URL de base
# Vérifier dans les scripts de test:
BASE_URL = "http://127.0.0.1:8000"  # ✅ Correct
BASE_URL = "http://localhost:8000"   # ⚠️ Peut poser problème

# 3. Problème de credentials
# Vérifier que le superuser existe:
poetry run python create_superuser.py
```

### 6. ❌ Erreurs JWT

**Symptômes :**
```
{"detail": "Given token not valid for any token type"}
{"detail": "Authentication credentials were not provided"}
```

**Solutions :**

```bash
# 1. Obtenir un nouveau token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}'

# 2. Vérifier le format du header
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

# 3. Token expiré - utiliser le refresh token
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### 7. ❌ Problèmes de permissions

**Symptômes :**
```
{"detail": "You do not have permission to perform this action."}
```

**Vérifications :**

```bash
# 1. Vérifier l'authentification
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/profile/

# 2. Vérifier les rôles et permissions
# - Seul l'auteur peut modifier/supprimer un projet
# - Seuls les contributeurs peuvent voir les détails
# - Seul l'auteur peut ajouter des contributeurs

# 3. Vérifier que l'utilisateur est contributeur
GET /api/projects/{id}/  # Doit être accessible
```

### 8. ❌ Problèmes de dépendances Poetry

**Symptômes :**
```
poetry install fails
Package not found
```

**Solutions :**

```bash
# 1. Nettoyer le cache Poetry
poetry cache clear --all pypi

# 2. Mettre à jour Poetry
poetry self update

# 3. Supprimer le lock file et réinstaller
del poetry.lock
poetry install

# 4. Forcer la réinstallation
poetry install --force

# 5. Vérifier Python version
poetry env use python3.12
```

## 🛠️ Outils de diagnostic

### Diagnostic automatique
```bash
# Script de diagnostic complet
poetry run python diagnose_project.py

# Test simple pour vérifier la configuration
poetry run python test_simple.py

# Vérification Django
poetry run python manage.py check --deploy
```

### Commandes de vérification

```bash
# Environnement Poetry
poetry env info
poetry show

# Configuration Django
poetry run python manage.py check
poetry run python manage.py showmigrations

# Base de données
poetry run python manage.py dbshell
poetry run python manage.py shell

# Tests de connectivité
curl http://127.0.0.1:8000/api/
curl http://127.0.0.1:8000/admin/
```

## 📋 Checklist de dépannage

### ✅ Vérifications basiques

- [ ] Je suis dans le bon répertoire (`manage.py` présent)
- [ ] Poetry est installé (`poetry --version`)
- [ ] Dépendances installées (`poetry install`)
- [ ] Migrations appliquées (`poetry run python manage.py migrate`)
- [ ] Superutilisateur créé (`poetry run python create_superuser.py`)

### ✅ Problèmes de tests

- [ ] J'utilise `poetry run python` (pas `python` directement)
- [ ] Le serveur Django est démarré pour les tests API
- [ ] L'encodage UTF-8 est configuré (`set PYTHONIOENCODING=utf-8`)
- [ ] Les credentials de test sont corrects

### ✅ Problèmes d'API

- [ ] Le serveur Django fonctionne (`poetry run python manage.py runserver`)
- [ ] L'API est accessible (`curl http://127.0.0.1:8000/api/`)
- [ ] Le token JWT est valide
- [ ] Les permissions sont correctes

## 🆘 Support et ressources

### Scripts de diagnostic
- `diagnose_project.py` - Diagnostic complet
- `test_simple.py` - Test de base
- `run_tests_universal.py` - Tests compatibles Windows

### Documentation
- `docs/ARCHITECTURE.md` - Architecture du projet
- `docs/TESTING_GUIDE.md` - Guide des tests
- `docs/API_GUIDE.md` - Documentation API

### Logs et debugging

```bash
# Logs Django détaillés
poetry run python manage.py runserver --verbosity=2

# Mode debug dans settings.py
DEBUG = True

# Shell Django pour debug
poetry run python manage.py shell
```

### Variables d'environnement utiles

```bash
# Windows CMD
set PYTHONIOENCODING=utf-8
set DJANGO_SETTINGS_MODULE=softdesk_support.settings
set PYTHONPATH=%CD%

# PowerShell
$env:PYTHONIOENCODING="utf-8"
$env:DJANGO_SETTINGS_MODULE="softdesk_support.settings"
$env:PYTHONPATH="."

# macOS/Linux
export PYTHONIOENCODING=utf-8
export DJANGO_SETTINGS_MODULE=softdesk_support.settings
export PYTHONPATH="."
```

## 🔧 Solutions rapides

### Réinitialisation complète
```bash
# Si tout est cassé, réinitialisation complète
del db.sqlite3
del poetry.lock
poetry install
poetry run python manage.py migrate
poetry run python create_superuser.py
poetry run python manage.py runserver
```

### Test de fonctionnement
```bash
# Vérification que tout fonctionne
poetry run python test_simple.py
poetry run python manage.py check
curl http://127.0.0.1:8000/api/
```

Ce guide devrait résoudre 95% des problèmes rencontrés avec le projet SoftDesk.
