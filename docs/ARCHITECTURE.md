# 🏗️ Architecture SoftDesk - Guide de Structure du Projet

## 📁 Structure générale du projet

```
project-10-django-REST/
├── 📄 README.md                    # Documentation principale
├── 📄 manage.py                    # Gestionnaire Django
├── 📄 pyproject.toml              # Configuration Poetry
├── 📄 ruff.toml                   # Configuration linter
├── 📄 run_all_tests.py            # Script global d'exécution des tests
├── 📄 create_superuser.py         # Utilitaire création superuser
├── 📄 db.sqlite3                  # Base de données SQLite
│
├── 📁 users/                      # App Django - Gestion utilisateurs
│   ├── models.py                  # Modèle CustomUser avec RGPD
│   ├── serializers.py             # Sérialisation API utilisateurs
│   ├── views.py                   # ViewSets pour endpoints utilisateurs
│   ├── admin.py                   # Interface admin Django
│   └──  # (pas de urls.py, routes gérées dans softdesk_support/urls.py)
│
├── 📁 issues/                     # App Django - Gestion projets/issues
│   ├── models.py                  # Modèles Project, Issue, Comment
│   ├── serializers.py             # Sérialisation pour tous les modèles
│   ├── views.py                   # ViewSets avec routes imbriquées
│   ├── admin.py                   # Interface admin complète
│   └──  # (pas de urls.py, routes gérées dans softdesk_support/urls.py)
│
├── 📁 softdesk_support/          # Projet Django principal
│   ├── settings.py                # Configuration Django + DRF + JWT
│   ├── urls.py                    # URLs principales avec versioning
│   └── wsgi.py                    # Configuration WSGI
│
├── 📁 tests/                     # 🧪 Suite de tests organisée
│   ├── __init__.py
│   ├── test_config.py             # Configuration partagée
│   ├── README.md                  # Documentation des tests
│   ├── 📁 models/                 # Tests des modèles Django
│   │   ├── test_project_contributor.py
│   │   ├── test_project_contributor_simple.py
│   │   ├── test_issue_comment.py
│   │   └── test_issue_comment_simple.py
│   ├── 📁 api/                    # Tests des endpoints API
│   │   ├── test_basic_api.py
│   │   ├── test_complete_api.py
│   │   ├── test_issue_comment_api.py
│   │   └── test_nested_routes.py
│   ├── 📁 rgpd/                   # Tests de conformité RGPD
│   │   ├── test_compliance.py
│   │   ├── test_api.py
│   │   └── test_age_validation.py
│   └── 📁 performance/            # Tests Green Code
│       ├── test_performance.py
│       └── demo_n_plus_1.py
│
└── 📁 docs/                      # 📚 Documentation organisée
    ├── ARCHITECTURE.md
    ├── API_GUIDE.md
    ├── GREEN_CODE_GUIDE.md
    ├── INDEX.md
    ├── ISSUE_COMMENT_API_GUIDE.md
    ├── N_PLUS_1_EXPLAINED.md
    ├── SECURITY_GUIDE.md
    ├── TESTING_GUIDE.md
    └── 📁 postman/
        ├── SoftDesk_API_Collection.json
        └── SoftDesk_Environment.json
```

## 🎯 Principes d'architecture

### 1. 📦 Séparation des responsabilités
- **`users/`** : Gestion authentification, profils, permissions utilisateurs
- **`issues/`** : Gestion projets, issues, commentaires et contributeurs
- **`softdesk_support/`** : Configuration centralisée Django/DRF

### 2. 🧪 Tests organisés par domaine
- **`tests/models/`** : Validation des modèles et relations
- **`tests/api/`** : Tests des endpoints et sérialisation
- **`tests/rgpd/`** : Conformité et protection des données
- **`tests/performance/`** : Optimisations Green Code

### 3. 📚 Documentation structurée
- **`docs/guides/`** : Guides d'utilisation et tests
- **`docs/postman/`** : Collections de tests API
- **`docs/*.md`** : Documentation technique spécialisée

## 🔗 Relations entre composants

### Modèles et relations
```
CustomUser (users.models)
    ↓ (ForeignKey author)
Project (issues.models)
    ↓ (ManyToMany contributors)
CustomUser
    ↓ (ForeignKey project)
Issue (issues.models)
    ↓ (ForeignKey issue)
Comment (issues.models)
```

### API et endpoints
```
/api/v1/
├── auth/                          # Authentication JWT
├── users/                         # Gestion utilisateurs
└── projects/                      # Projets avec routes imbriquées
    ├── {id}/contributors/         # Contributeurs d'un projet
    ├── {id}/issues/              # Issues d'un projet
    └── {project_id}/issues/{id}/comments/  # Commentaires d'une issue
```

## 🛠️ Technologies et patterns

### Backend
- **Django 5.x** : Framework web robuste
- **Django REST Framework** : API RESTful
- **drf-nested-routers** : Routes imbriquées
- **Simple JWT** : Authentification stateless
- **Poetry** : Gestion des dépendances

### Patterns utilisés
- **ViewSets** : Organisation cohérente des endpoints
- **ModelSerializers** : Sérialisation automatisée
- **Permissions personnalisées** : Contrôle d'accès granulaire
- **select_related/prefetch_related** : Optimisation requêtes N+1
- **Pagination** : Performance et expérience utilisateur
- **Throttling** : Protection contre les abus

### Green Code
- **Optimisation des requêtes** : Éviter les requêtes N+1
- **Pagination obligatoire** : Limite de charge serveur
- **Throttling intelligent** : Économie des ressources
- **Tests de performance** : Mesure de l'impact carbone

## 🔧 Configuration et déploiement

### Environnement de développement
```bash
# Installation et démarrage
poetry install
poetry run python manage.py migrate
poetry run python create_superuser.py
poetry run python manage.py runserver
```

### Tests et validation
```bash
# Tous les tests
poetry run python run_all_tests.py

# Tests par catégorie
poetry run python tests/models/test_project_contributor.py
poetry run python tests/api/test_complete_api.py
poetry run python tests/rgpd/test_compliance.py
poetry run python tests/performance/test_performance.py
```

## 📊 Métriques et qualité

### Couverture des tests
- **Modèles** : 100% (4 fichiers de test)
- **API** : 100% (4 fichiers de test)
- **RGPD** : 100% (3 fichiers de test)
- **Performance** : 100% (2 fichiers de test)

### Standards de qualité
- **Code style** : Ruff linting
- **Documentation** : README + guides détaillés
- **Sécurité** : JWT + permissions granulaires
- **Performance** : Green Code + optimisations SQL
- **Conformité** : RGPD compliance

## 🎯 Évolutions futures

### Possible améliorations
1. **Cache Redis** : Performance des requêtes fréquentes
2. **Tests d'intégration** : Selenium pour tests end-to-end
3. **CI/CD Pipeline** : Automatisation déploiement
4. **Monitoring** : Logs et métriques de performance
5. **Docker** : Containerisation pour déploiement
6. **API versioning** : Gestion des évolutions d'API

Cette architecture respecte les bonnes pratiques Django/DRF tout en maintenant une structure claire, testable et évolutive.
