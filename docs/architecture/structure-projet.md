# 📁 Structure du Projet

[← Retour à l'architecture](./README.md)

## 🗂️ Organisation des fichiers

```
project-10-django-REST/
├── 📁 softdesk_support/          # Configuration principale Django
│   ├── __init__.py
│   ├── settings.py              # Configuration Django
│   ├── urls.py                  # Routes principales
│   └── wsgi.py                  # Point d'entrée WSGI
│
├── 📁 users/                    # Application utilisateurs
│   ├── models.py               # Modèle User personnalisé
│   ├── views.py                # ViewSets utilisateurs
│   ├── serializers.py          # Serializers utilisateurs
│   └── admin.py                # Configuration admin
│
├── 📁 issues/                   # Application principale
│   ├── models.py               # Project, Issue, Comment, Contributor
│   ├── views.py                # ViewSets principaux
│   ├── serializers.py          # Serializers principaux
│   ├── permissions.py          # Permissions personnalisées
│   └── admin.py                # Configuration admin
│
├── 📁 docs/                     # Documentation
│
├── 📄 manage.py                 # Script de gestion Django
├── 📄 pyproject.toml           # Configuration Poetry
├── 📄 poetry.lock              # Verrous de dépendances
├── 📄 README.md                # Documentation principale
└── 📄 .gitignore              # Fichiers ignorés par Git
```

## 🔧 Applications Django

### 1. **users** - Gestion des utilisateurs
- Modèle User personnalisé avec champs RGPD
- Authentification et création de compte
- Gestion des profils

### 2. **issues** - Cœur de l'application
- **Models** :
  - `Project` : Projets de développement
  - `Issue` : Problèmes/tâches
  - `Comment` : Commentaires sur les issues
  - `Contributor` : Liens utilisateurs-projets
  
- **ViewSets** :
  - `ProjectViewSet` : CRUD projets
  - `IssueViewSet` : CRUD issues
  - `CommentViewSet` : CRUD commentaires
  - `ContributorViewSet` : Gestion contributeurs

## 🔌 Configuration

### URLs imbriquées
```python
/api/projects/                              # Projets
/api/projects/{id}/contributors/            # Contributeurs d'un projet
/api/projects/{id}/issues/                  # Issues d'un projet
/api/projects/{id}/issues/{id}/comments/    # Commentaires d'une issue
```

### Settings modulaires
- Configuration de base dans `settings.py`
- Variables d'environnement supportées
- Configuration JWT personnalisée
- Pagination et throttling configurés

## 📝 Conventions

1. **Nommage** :
   - Apps : nom au pluriel (`users`, `issues`)
   - Models : nom au singulier (`User`, `Project`)
   - ViewSets : nom + ViewSet (`ProjectViewSet`)

2. **Organisation** :
   - Un fichier par type (models, views, serializers)
   - Permissions dans un fichier séparé
   - Tests dans des dossiers `tests/`

3. **Imports** :
   ```python
   # 1. Standard library
   import os
   
   # 2. Django
   from django.db import models
   
   # 3. Third party
   from rest_framework import viewsets
   
   # 4. Local
   from .models import Project
   ```
