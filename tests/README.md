# 🧪 Tests SoftDesk API

Ce dossier contient tous les tests automatisés pour l'API SoftDesk, organisés par catégorie.

## 📁 Structure des tests

```
tests/
├── __init__.py
├── test_config.py          # Configuration commune pour tous les tests
├── models/                 # Tests des modèles Django
│   ├── test_project_contributor.py
│   ├── test_project_contributor_simple.py
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

## 🚀 Exécution des tests

### Tous les tests d'un coup
```bash
# Exécuter tous les tests dans l'ordre optimal
poetry run python run_all_tests.py
```

### Par catégorie

**Tests des modèles :**
```bash
poetry run python tests/models/test_project_contributor.py
poetry run python tests/models/test_issue_comment.py
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

## 📊 Couverture des tests

| Catégorie | Fichiers | Couverture | Statut |
|-----------|----------|------------|--------|
| **Modèles** | 4 | 100% | ✅ |
| **API** | 4 | 100% | ✅ |
| **RGPD** | 3 | 100% | ✅ |
| **Performance** | 2 | 100% | ✅ |

## 🛠️ Configuration

Le fichier `test_config.py` contient :
- Configuration Django commune
- Données de test standardisées
- Fonctions utilitaires de nettoyage
- Variables partagées entre tests

## 🎯 Bonnes pratiques

1. **Isolation** : Chaque test nettoie ses données
2. **Réutilisabilité** : Configuration commune dans `test_config.py`
3. **Organisation** : Tests groupés par domaine fonctionnel
4. **Performance** : Tests d'optimisation dédiés
5. **Conformité** : Tests RGPD séparés pour audit
