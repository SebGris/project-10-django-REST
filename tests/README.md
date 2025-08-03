# 🧪 Tests SoftDesk API

[← Retour à la documentation](../docs/README.md)

Ce dossier contient tous les tests automatisés pour l'API SoftDesk, organisés par catégorie.

## 📋 Vue d'ensemble

Cette section couvre les différentes stratégies de test pour l'API SoftDesk, incluant les tests unitaires, d'intégration et les collections Postman.

## 📁 Structure des tests

```
tests/
├── __init__.py
├── test_config.py          # Configuration commune pour tous les tests
├── models/                 # Tests des modèles Django
│   ├── test_issue_comment.py
│   └── test_issue_comment_simple.py
├── api/                    # Tests des endpoints API
│   ├── test_basic_api.py
│   ├── test_complete_api.py
│   ├── test_issue_comment_api.py
│   └── test_nested_routes.py
├── rgpd/                   # Tests de conformité RGPD
│   ├── test_compliance.py
│   ├── test_api.py
│   └── test_age_validation.py
└── performance/            # Tests de performance et optimisations
    ├── test_performance.py
    └── demo_n_plus_1.py
```

Par ailleurs, chaque application Django possède ses propres tests :

```
issues/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_serializers.py
│   └── test_permissions.py
```

## 📚 Documentation des tests

### 1. Tests unitaires
- Tests des modèles
- Tests des serializers
- Tests des permissions

### 2. Tests d'intégration
- Tests des ViewSets
- Tests des endpoints
- Tests du workflow complet

### 3. Collection Postman
- Voir le [Guide Postman](../docs/postman/postman-guide.md) pour l'utilisation de la collection de tests
- Import de la collection
- Variables d'environnement
- Scénarios de test

## 🚀 Exécution des tests

### Tous les tests d'un coup
```bash
# Exécuter tous les tests dans l'ordre optimal
poetry run python run_all_tests.py

# Tous les tests avec Django
poetry run python manage.py test

# Tests avec coverage
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

### Par catégorie

**Tests des modèles :**
```bash
# Avec le runner de tests spécifique
poetry run python tests/models/test_issue_comment.py

# Avec Django
poetry run python manage.py test issues
```

**Tests des API :**
```bash
poetry run python tests/api/test_basic_api.py
poetry run python tests/api/test_complete_api.py
```

**Tests RGPD :**
```bash
poetry run python tests/rgpd/test_compliance.py
```

**Tests de performance :**
```bash
poetry run python tests/performance/test_performance.py
```

## 📊 Métriques et couverture

### Coverage cible
- **Global** : > 80%
- **Models** : > 90%
- **Views** : > 85%
- **Serializers** : > 80%

### Couverture actuelle des tests

| Catégorie | Fichiers | Couverture | Statut |
|-----------|----------|------------|--------|
| **Modèles** | 4 | 100% | ✅ |
| **API** | 4 | 100% | ✅ |
| **RGPD** | 3 | 100% | ✅ |
| **Performance** | 2 | 100% | ✅ |

### Types de tests
1. **Unitaires** : Logique isolée
2. **Intégration** : Interaction entre composants
3. **E2E** : Workflow complet via Postman
4. **Performance** : Temps de réponse

## 🛠️ Configuration

Le fichier `test_config.py` contient :
- Configuration Django commune
- Données de test standardisées
- Fonctions utilitaires de nettoyage
- Variables partagées entre tests

## 🔧 Outils utilisés

- **pytest-django** : Framework de test
- **factory-boy** : Création de données de test
- **coverage.py** : Couverture de code
- **Postman** : Tests API manuels/automatisés

## 🎯 Bonnes pratiques

1. **Isolation** : Chaque test nettoie ses données
2. **Réutilisabilité** : Configuration commune dans `test_config.py`
3. **Organisation** : Tests groupés par domaine fonctionnel
4. **Performance** : Tests d'optimisation dédiés
5. **Conformité** : Tests RGPD séparés pour audit

## ✅ Checklist de test

- [ ] Tous les modèles ont des tests
- [ ] Toutes les permissions sont testées
- [ ] Les cas d'erreur sont couverts
- [ ] Les workflows principaux sont testés
- [ ] La collection Postman est à jour
- [ ] Les tests passent en CI/CD
