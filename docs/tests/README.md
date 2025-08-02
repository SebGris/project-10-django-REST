# 🧪 Guide de Tests

[← Retour à la documentation](../README.md)

## 📋 Vue d'ensemble

Cette section couvre les différentes stratégies de test pour l'API SoftDesk, incluant les tests unitaires, d'intégration et les collections Postman.

## 📚 Contenu

### 1. [Tests unitaires](./tests-unitaires.md)
- Tests des modèles
- Tests des serializers
- Tests des permissions

### 2. [Tests d'intégration](./tests-integration.md)
- Tests des ViewSets
- Tests des endpoints
- Tests du workflow complet

### 3. [Collection Postman](./postman-collection.md)
- Import de la collection
- Variables d'environnement
- Scénarios de test

## 🚀 Lancer les tests

### Tests Django
```bash
# Tous les tests
poetry run python manage.py test

# Tests d'une app spécifique
poetry run python manage.py test issues

# Tests avec coverage
poetry run coverage run --source='.' manage.py test
poetry run coverage report
```

### Structure des tests
```
issues/
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   ├── test_serializers.py
│   └── test_permissions.py
```

## 📊 Métriques de qualité

### Coverage cible
- **Global** : > 80%
- **Models** : > 90%
- **Views** : > 85%
- **Serializers** : > 80%

### Types de tests
1. **Unitaires** : Logique isolée
2. **Intégration** : Interaction entre composants
3. **E2E** : Workflow complet via Postman
4. **Performance** : Temps de réponse

## 🔧 Outils utilisés

- **pytest-django** : Framework de test
- **factory-boy** : Création de données de test
- **coverage.py** : Couverture de code
- **Postman** : Tests API manuels/automatisés

## ✅ Checklist de test

- [ ] Tous les modèles ont des tests
- [ ] Toutes les permissions sont testées
- [ ] Les cas d'erreur sont couverts
- [ ] Les workflows principaux sont testés
- [ ] La collection Postman est à jour
- [ ] Les tests passent en CI/CD
