# 🌐 Projet 10 Django REST
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

1. **Fermer cette fenêtre de terminal**
2. **Ouvrir un nouveau terminal**
3. **Ou redémarrer VS Code**

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
Tapez Ctrl+C pour arrêter le serveur.

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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

🚀 Commande pour créer le superutilisateur
```bash
poetry run python manage.py createsuperuser
```

Puis suivez les instructions :
Username: admin
Email address: admin@softdesk.local
Password: SoftDesk2025!
Password (again): SoftDesk2025!

🔒 Note de sécurité
⚠️ Important : Ces mots de passe sont à usage de développement uniquement. En production, utilisez toujours des mots de passe forts et uniques !
## Lancement du projet en local

TODO

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
   - `GET/POST /api/projects/` - Lister/Créer des projets
   - `GET/PUT/DELETE /api/projects/{id}/` - Détails/Modifier/Supprimer
   - `POST /api/projects/{id}/add-contributor/` - Ajouter contributeur

### **Étape 4 : Script de test automatique**
```bash
# Installer requests si nécessaire
poetry add requests

# Exécuter le script de test
poetry run python test_api.py
```

### **Étape 5 : Interface web**
Accédez à http://127.0.0.1:8000/api/ pour l'interface Django REST Framework

## 📊 Endpoints de l'API

| Méthode | URL | Description | Auth |
|---------|-----|-------------|------|
| POST | `/api/token/` | Obtenir token JWT | Non |
| GET | `/api/projects/` | Lister projets | Oui |
| POST | `/api/projects/` | Créer projet | Oui |
| GET | `/api/projects/{id}/` | Détails projet | Oui |
| PUT | `/api/projects/{id}/` | Modifier projet | Auteur |
| DELETE | `/api/projects/{id}/` | Supprimer projet | Auteur |
| POST | `/api/projects/{id}/add-contributor/` | Ajouter contributeur | Auteur |

## 📄 Aide
- [Poetry le gestionnaire de dépendances Python moderne](https://blog.stephane-robert.info/docs/developper/programmation/python/poetry/)
- [pipx — Install and Run Python Applications in Isolated Environments](https://pipx.pypa.io/stable/)
- [Setting up a basic Django project with Poetry](https://builtwithdjango.com/blog/basic-django-setup)
- [Poetry — Installation](https://python-poetry.org/docs/#installing-with-pipx)
- [Getting started — Simple JWT documentation](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration)