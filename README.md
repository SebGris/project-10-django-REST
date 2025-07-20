# 🌐 Projet 10 - Créez une API sécurisée RESTful
API développée avec Django REST dans le cadre d'un projet de formation OpenClassrooms Développeur d'application Python.

## Installation du projet en local
### Installation de Poetry
#### **Étape 1 : Installation de pipx**
```bash
python -m pip install --user pipx
```

#### **Étape 2 : Ajouter pipx au PATH**
```bash
python -m pipx ensurepath
```
**Pour que les changements prennent effet, vous devez :**

**redémarrer VS Code**

Après cela, vous pourrez utiliser directement `pipx` au lieu de `python -m pipx`.

#### **Étape 3 : Installation de Poetry**

```bash
pipx install poetry
```

#### **Étape 4 : Vérification de l’installation**

```bash
poetry --version
```

### Utilisation de Poetry
#### **Étape 1 : Créer un projet**
Poetry configure tout pour vous, générant un fichier `pyproject.toml` pour centraliser la configuration.
```bash
poetry init
```
Vous serez guidé à travers une série de questions interactives :
- Nom du projet
- Version initiale
- Description
- Auteur(s)
- Dépendances et compatibilité Python

Si vous préférez sauter les questions, utilisez l’option `--no-interaction` pour une initialisation rapide avec des valeurs par défaut.
```bash
poetry init --no-interaction
``` 

#### **Étape 2 : Ajouter des dépendances**
Pour ajouter une dépendance dans un projet Poetry, il suffit de faire :
```bash
poetry add Django
poetry add djangorestframework
``` 

#### **Étape 3 : Activer l’environnement virtuel**
```bash
poetry env activate
``` 
Ensuite, Poetry vous donne le chemin vers le script d'activation de l'environnement virtuel. Cette réponse est normale avec `poetry env activate` - elle vous indique où se trouve le script d'activation.

```bash
C:\Users\_votre_user_\AppData\Local\pypoetry\Cache\virtualenvs\project-10-django-rest-nlqPrlS_-py3.12\Scripts\activate.bat
``` 

### Utilisation de Django
#### **Étape 1 : Créer un nouveau projet**
Lançons un projet Django à l'aide de la commande Django admin :
```bash
poetry run django-admin startproject softdesk_support .
```
Pour tester que tout est configuré comme il se doit, lançons le serveur local :
```bash
poetry run python manage.py runserver
```
Tapez Ctrl+c pour arrêter le serveur.

#### **Étape 2 : Créer la base de données du projet**
Appliquez les migrations initiales :
```bash
poetry run python manage.py migrate
```

#### **Étape 3 : Créer une application**
```bash
poetry run python manage.py startapp issues
cd softdesk_support
```
#### **Étape 4 : Configurer l'application**
Ajouter votre application dans `settings.py` :
```python
INSTALLED_APPS = [
    ...
    'rest_framework',  # Django REST Framework
    'issues',          # Votre application
]
```
##### Tester le serveur de développement
Démarrez le serveur pour vérifier que tout fonctionne :
```bash
poetry run python manage.py runserver
```
Ouvrez http://127.0.0.1:8000/ dans votre navigateur pour vérifier que le site Django fonctionne.
Tapez Ctrl+C pour arrêter le serveur.

### Ajoutez l’authentification des utilisateurs
#### **Étape 1 : Installer djangorestframework-simple-jwt**

```bash
poetry add djangorestframework-simplejwt
``` 
#### **Étape 2 : Configurer djangorestframework-simple-jwt**
Ajouter JWT dans les applications Django dans `settings.py` :
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt', # JWT Authentication
    'issues',
]
```
Ensuite, votre projet django doit être configuré pour utiliser la bibliothèque. Dans `settings.py`, ajoutez `rest_framework_simplejwt.authentication.JWTAuthentication` à la liste des classes d'authentification :
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
```
De plus, dans votre fichier `urls.py`, incluez des routes pour les vues `TokenObtainPairView` et `TokenRefreshView` de Simple JWT :
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

## Lancement du projet en local

#### **Étape 1 : Installer toutes les dépendances définies dans pyproject.toml**
```bash
poetry install
```

#### **Étape 2 : Créer et appliquer les migrations (dans le bon ordre)**
⚠️ **Important** : L'app `users` doit être migrée en premier car elle contient le modèle User personnalisé.

```bash
# 1. Créer les migrations pour l'app users (modèle User personnalisé)
poetry run python manage.py makemigrations users

# 2. Créer les migrations pour l'app issues
poetry run python manage.py makemigrations issues

# 3. Créer toutes les autres migrations
poetry run python manage.py makemigrations

# 4. Appliquer toutes les migrations
poetry run python manage.py migrate
```

#### **Étape 3 : Créer un superutilisateur**
🚀 **Méthode recommandée** : Utiliser notre script personnalisé qui gère tous les champs obligatoires
```bash
poetry run python create_superuser.py
```

🔄 **Méthode alternative** : Commande Django standard (peut causer des erreurs avec les champs obligatoires)
```bash
poetry run python manage.py createsuperuser
```

⚠️ **Note importante** : Si vous utilisez la commande standard et obtenez l'erreur `This field cannot be null`, utilisez le script personnalisé à la place.

✅ **Informations de connexion par défaut** :
- Username: `admin`
- Email: `admin@softdesk.local`  
- Password: `SoftDesk2025!`
- Âge: 30 ans (conforme RGPD)

🔒 Note de sécurité
⚠️ Important : Ces mots de passe sont à usage de développement uniquement. En production, utilisez toujours des mots de passe forts et uniques !

## 🔐 Conformité RGPD

⚠️ **Validation d'âge obligatoire** : Conformément au RGPD, les utilisateurs de moins de 15 ans ne peuvent pas s'inscrire sur la plateforme.

### Test de la conformité RGPD
```bash
# Tester la validation d'âge
poetry run python test_rgpd_compliance.py
```

Ce test vérifie que :
- ❌ Les utilisateurs de moins de 15 ans sont rejetés
- ✅ Les utilisateurs de 15 ans et plus sont acceptés  
- 📝 Les messages d'erreur sont appropriés

### Test des modèles Issue et Comment
```bash
# Tester les modèles Issue et Comment
poetry run python test_issue_comment_models.py
```

### Test complet de l'API complète
```bash
# Tester tous les endpoints (users, projects, issues, comments)
poetry run python test_etape4_complete.py
```

Ce test vérifie que :
- ✅ Configuration Django valide
- ✅ Migrations appliquées correctement  
- ✅ Tous les modèles fonctionnent (User, Project, Contributor, Issue, Comment)
- ✅ Endpoints API accessibles et fonctionnels

#### **Étape 4 : Démarrer le serveur de développement**
```bash
poetry run python manage.py runserver
```

## 🏗️ Architecture simplifiée

✅ **URLs centralisées** : Tous les endpoints sont définis dans un seul fichier `softdesk_support/urls.py` pour une meilleure lisibilité et maintenance.

✅ **ViewSets organisés** : 
- `UserViewSet` dans `users/views.py`
- `ProjectViewSet`, `ContributorViewSet`, `IssueViewSet`, `CommentViewSet` dans `issues/views.py`

✅ **Routeur unique** : Django REST Framework router gère automatiquement tous les endpoints CRUD.

## 🚨 Résolution des problèmes de migration

Si vous rencontrez l'erreur `InconsistentMigrationHistory`, suivez ces étapes :

1. **Supprimer la base de données** (⚠️ perte de données) :
```bash
del db.sqlite3
```

2. **Supprimer tous les fichiers de migration** :
```bash
del issues\migrations\*.py
del users\migrations\*.py
```

3. **Recréer les fichiers __init__.py** dans les dossiers migrations

4. **Recréer les migrations dans le bon ordre** (voir Étape 2 ci-dessus)

## 🧪 Tester l'API

### **Étape 1 : Démarrer le serveur**
```bash
poetry run python manage.py runserver
```

### **Étape 2 : Créer un utilisateur de test**
Option 1 : Utiliser le superutilisateur créé
Option 2 : Créer via l'interface admin à http://127.0.0.1:8000/admin/

### **Étape 3 : Tester avec Postman**
1. **Obtenir un token JWT :**
   - POST `http://127.0.0.1:8000/api/token/`
   - Body: `{"username": "admin", "password": "SoftDesk2025!"}`

2. **Ajouter l'authentification :**
   - Header: `Authorization: Bearer YOUR_TOKEN`

3. **Endpoints disponibles :**
   
   **🧑‍💼 API Utilisateurs :**
   - `POST /api/users/` - Inscription (sans auth)
   - `GET /api/users/` - Liste des utilisateurs
   - `GET /api/users/{id}/` - Détails d'un utilisateur
   - `GET/PUT/PATCH /api/users/profile/` - Profil personnel
   
   **📋 API Projets :**
   - `GET/POST /api/projects/` - Lister/Créer des projets
   - `GET/PUT/DELETE /api/projects/{id}/` - Détails/Modifier/Supprimer
   - `POST /api/projects/{id}/add-contributor/` - Ajouter contributeur

### **Étape 4 : Guide de test détaillé**

🧪 **Trois méthodes pour tester l'API :**

**Option A : Script automatique (Recommandé)**
```bash
# Installer requests si nécessaire
pip install requests

# Lancer le script de test complet
python test_api_complete.py
```

**Option B : Collection Postman**
1. Importer `SoftDesk_API_Postman_Collection.json` dans Postman
2. Configurer l'environnement avec `base_url: http://127.0.0.1:8000`
3. Exécuter les requêtes dans l'ordre

**Option C : Interface DRF**
Accédez à `http://127.0.0.1:8000/api/` pour une interface graphique

📋 **Guides détaillés :**
- `API_TESTING_COMPLETE_GUIDE.md` - Guide complet étape par étape
- `USERS_API_TESTING.md` - Focus sur les endpoints utilisateurs
- `ISSUE_COMMENT_API_GUIDE.md` - Guide rapide pour tester Issues et Comments

### **Étape 5 : Script de test automatique**
```bash
# Installer requests si nécessaire
poetry add requests

# Exécuter le script de test
poetry run python test_api.py
```

### **Étape 6 : Interface web**
Accédez à http://127.0.0.1:8000/api/ pour l'interface Django REST Framework

## 📊 Endpoints de l'API

### 🧑‍💼 API Utilisateurs
| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/users/` | Inscription utilisateur | Non |
| GET | `/api/users/` | Lister utilisateurs | Oui |
| GET | `/api/users/{id}/` | Détails utilisateur | Oui |
| GET | `/api/users/profile/` | Profil personnel | Oui |
| PUT/PATCH | `/api/users/profile/` | Modifier profil | Oui |
| DELETE | `/api/users/{id}/` | Supprimer compte | Oui |

### 📋 API Projets
| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/token/` | Obtenir token JWT | Non |
| GET | `/api/projects/` | Lister projets | Oui |
| POST | `/api/projects/` | Créer projet | Oui |
| GET | `/api/projects/{id}/` | Détails projet | Oui |
| PUT | `/api/projects/{id}/` | Modifier projet | Auteur |
| DELETE | `/api/projects/{id}/` | Supprimer projet | Auteur |
| POST | `/api/projects/{id}/add-contributor/` | Ajouter contributeur | Auteur |

### 🐛 API Issues
| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | `/api/issues/` | Lister issues | Oui |
| POST | `/api/issues/` | Créer issue | Contributeur |
| GET | `/api/issues/{id}/` | Détails issue | Contributeur |
| PUT | `/api/issues/{id}/` | Modifier issue | Auteur/Propriétaire |
| DELETE | `/api/issues/{id}/` | Supprimer issue | Auteur/Propriétaire |

### 💬 API Commentaires
| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| GET | `/api/comments/` | Lister commentaires | Oui |
| POST | `/api/comments/` | Créer commentaire | Contributeur |
| GET | `/api/comments/{id}/` | Détails commentaire | Contributeur |
| PUT | `/api/comments/{id}/` | Modifier commentaire | Auteur |
| DELETE | `/api/comments/{id}/` | Supprimer commentaire | Auteur/Propriétaire |

## 📄 Aide
- [Poetry le gestionnaire de dépendances Python moderne](https://blog.stephane-robert.info/docs/developper/programmation/python/poetry/)
- [pipx — Install and Run Python Applications in Isolated Environments](https://pipx.pypa.io/stable/)
- [Setting up a basic Django project with Poetry](https://builtwithdjango.com/blog/basic-django-setup)
- [Poetry — Installation](https://python-poetry.org/docs/#installing-with-pipx)
- [Getting started — Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration)