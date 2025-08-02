# 🔧 Guides de Développement

[← Retour à la documentation](../README.md)

## 📋 Guides disponibles

### Django ORM
- [Get_or_create et defaults](./get-or-create-defaults.md) - Pattern de création/récupération

### À venir
- ViewSets et permissions
- Serializers avancés
- Tests unitaires Django
- Gestion des migrations

## 🎯 Navigation rapide

| Guide | Description |
|-------|-------------|
| [get_or_create](./get-or-create-defaults.md) | Comprendre get_or_create et le paramètre defaults |
   - Serializers en lecture/écriture
   - Optimisation des performances

### Guides pratiques

4. **[Optimisation des requêtes](./querysets-optimisation.md)**
   - select_related() et prefetch_related()
   - Éviter les requêtes N+1
   - Monitoring des performances

5. **[Gestion des erreurs](./gestion-erreurs.md)**
   - Exceptions personnalisées
   - Messages d'erreur cohérents
   - Logging et debugging

## 🚀 Quick Links

| Sujet | Description | Niveau |
|-------|-------------|---------|
| [get_or_create()](./get-or-create-defaults.md) | Création conditionnelle d'objets | Débutant |
| [ViewSets](./viewsets-permissions.md) | Architecture REST | Intermédiaire |
| [Permissions](./viewsets-permissions.md#permissions) | Sécurité et autorisations | Intermédiaire |
| [Serializers](./serializers-relations.md) | Transformation des données | Avancé |
| [Optimisations](./querysets-optimisation.md) | Performance SQL | Avancé |

## 📝 Conventions de code

```python
# Imports organisés par groupe
from django.db import models  # Django
from rest_framework import viewsets  # DRF
from .models import Project  # Local

# Docstrings descriptives
def ma_fonction():
    """Description claire de ce que fait la fonction."""
    pass

# Noms explicites
user_projects = Project.objects.filter(author=user)  # ✅
p = Project.objects.filter(a=u)  # ❌
```

## 🔗 Ressources externes

- [Documentation Django](https://docs.djangoproject.com/)
- [Documentation DRF](https://www.django-rest-framework.org/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
