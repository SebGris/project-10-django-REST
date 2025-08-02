# 🧪 Guide de Tests

[← Retour à la documentation](../README.md)

## 📋 Redirection

> **Documentation déplacée** : La documentation complète des tests se trouve maintenant dans le [README.md du dossier tests](../../tests/README.md).

Ce fichier a été fusionné avec le README.md du dossier tests pour éviter la duplication d'information et maintenir une source unique de vérité concernant les tests.

Veuillez consulter le [README.md du dossier tests](../../tests/README.md) pour accéder à la documentation complète des tests, incluant :

- Structure des tests
- Exécution des tests
- Documentation des tests
- Métriques et couverture
- Configuration
- Outils utilisés
- Bonnes pratiques
- Checklist de test

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
