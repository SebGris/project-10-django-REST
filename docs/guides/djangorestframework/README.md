# 🌐 Guides Django REST Framework

[← Retour aux guides](../README.md)

## 📚 Guides disponibles

### [DefaultRouter](./defaultrouter-guide.md)
Le routeur automatique de DRF :
- Génération automatique d'URLs
- Configuration et utilisation
- Routes générées par défaut
- Personnalisation avancée

### [ModelViewSet](./modelviewset-guide.md)
ViewSets pour API CRUD complète :
- Actions automatiques (list, create, retrieve, update, destroy)
- Personnalisation des queryset
- Actions personnalisées avec @action
- Permissions et filtrage

### [Routes imbriquées](./nested-router-guide.md)
NestedDefaultRouter pour URLs hiérarchiques :
- Relations parent-enfant dans les URLs
- Configuration des routes imbriquées
- Accès aux paramètres parents
- Bonnes pratiques RESTful

## 🎯 Ordre de lecture recommandé

1. **[ModelViewSet](./modelviewset-guide.md)** - Comprendre les ViewSets
2. **[DefaultRouter](./defaultrouter-guide.md)** - Maîtriser le routage
3. **[Routes imbriquées](./nested-router-guide.md)** - URLs avancées

## 🔧 Dans le projet SoftDesk

Ces concepts sont utilisés dans :
- `softdesk_support/urls.py` - Configuration des routes
- `issues/views.py` - ViewSets principaux
- `users/views.py` - ViewSet utilisateurs

## 🔗 Ressources DRF

- [Documentation officielle DRF](https://www.django-rest-framework.org/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Best Practices](https://github.com/encode/django-rest-framework/tree/master/docs)
