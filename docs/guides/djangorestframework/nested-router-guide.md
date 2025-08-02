# 🛣️ Routes SoftDesk - Guide des URL Imbriquées (NestedDefaultRouter)

[← Retour à la documentation](./README.md) | [DefaultRouter Guide](./defaultrouter-guide.md) | [Architecture](../../architecture/architecture.md)

## 📋 Navigation
- [Vue d'ensemble](#vue-densemble)
- [Configuration des routes](#configuration-des-routes)
- [ViewSets imbriqués](#viewsets-imbriqués)
- [Permissions et sécurité](#permissions-et-sécurité)
- [Tests des routes](../../api/api-testing-complete-guide.md)

## 🎯 **Qu'est-ce que NestedDefaultRouter ?**

`NestedDefaultRouter` permet de créer des **routes imbriquées** (nested routes) qui respectent l'architecture REST hiérarchique.

**Package requis :** `djangorestframework-nested`

## 🏗️ **Différence conceptuelle**

### ❌ **Routes plates (DefaultRouter classique)**
```python
/api/projects/          # Tous les projets
# Accès imbriqué uniquement (RESTful)
/api/projects/{project_id}/issues/            # Issues d'un projet
/api/projects/{project_id}/issues/{issue_id}/comments/   # Commentaires d'une issue
```
**Problème :** Pas de contexte, sécurité complexe à gérer

### ✅ **Routes imbriquées (NestedDefaultRouter)**
```python
/api/projects/1/issues/                     # Issues DU projet 1 seulement
/api/projects/1/issues/5/comments/          # Commentaires DE l'issue 5 DU projet 1
```
**Avantage :** Contexte clair, sécurité automatique

## 📋 **Syntaxe de base**

```python
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# 1. Routeur principal
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)

# 2. Routeur imbriqué
nested_router = routers.NestedDefaultRouter(
    parent_router=router,           # Routeur parent
    parent_prefix=r'projects',      # Préfixe parent dans l'URL
    lookup='project'                # Nom du paramètre (project_pk)
)
nested_router.register(r'issues', IssueViewSet)

# 3. Dans urlpatterns
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(nested_router.urls)),
]
```

## 🌐 **Exemple complet : SoftDesk**

### **Configuration dans urls.py**
```python
# Niveau 0 : Routeur principal
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')

# Niveau 1 : Routes imbriquées pour les projets
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

# Niveau 2 : Routes imbriquées pour les issues
issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),
    path('api/', include(issues_router.urls)),
]
```

### **URLs générées automatiquement**
```bash
# Niveau 0 - Projets
GET    /api/projects/                    # Liste projets
POST   /api/projects/                    # Créer projet
GET    /api/projects/{id}/               # Détails projet
PUT    /api/projects/{id}/               # Modifier projet
DELETE /api/projects/{id}/               # Supprimer projet

# Niveau 1 - Contributeurs d'un projet
GET    /api/projects/{project_pk}/contributors/           # Liste contributeurs
POST   /api/projects/{project_pk}/contributors/           # Ajouter contributeur
DELETE /api/projects/{project_pk}/contributors/{id}/      # Retirer contributeur

# Niveau 1 - Issues d'un projet
GET    /api/projects/{project_pk}/issues/                 # Issues du projet
POST   /api/projects/{project_pk}/issues/                 # Créer issue
GET    /api/projects/{project_pk}/issues/{id}/            # Détails issue
PUT    /api/projects/{project_pk}/issues/{id}/            # Modifier issue
DELETE /api/projects/{project_pk}/issues/{id}/            # Supprimer issue

# Niveau 2 - Commentaires d'une issue
GET    /api/projects/{project_pk}/issues/{issue_pk}/comments/        # Liste commentaires
POST   /api/projects/{project_pk}/issues/{issue_pk}/comments/        # Créer commentaire
GET    /api/projects/{project_pk}/issues/{issue_pk}/comments/{id}/   # Détails commentaire
PUT    /api/projects/{project_pk}/issues/{issue_pk}/comments/{id}/   # Modifier commentaire
DELETE /api/projects/{project_pk}/issues/{issue_pk}/comments/{id}/   # Supprimer commentaire
```

## 🔧 **Utilisation dans les ViewSets**

### **Récupération des paramètres parents**
```python
class IssueViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # project_pk est automatiquement disponible !
        project_pk = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=project_pk)
    
    def perform_create(self, serializer):
        # Récupérer le projet parent
        project_pk = self.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_pk)
        serializer.save(project=project)

class CommentViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Les deux paramètres sont disponibles !
        project_pk = self.kwargs['project_pk']
        issue_pk = self.kwargs['issue_pk']
        return Comment.objects.filter(
            issue_id=issue_pk,
            issue__project_id=project_pk
        )
```

### **Paramètres automatiques disponibles**
```python
# Dans un ViewSet imbriqué, vous avez accès à :
self.kwargs['project_pk']    # ID du projet parent
self.kwargs['issue_pk']      # ID de l'issue parent (si niveau 2)
self.kwargs['pk']            # ID de l'objet actuel
```

## 🎯 **Paramètres importants**

### **lookup**
```python
# lookup='project' génère le paramètre 'project_pk'
# lookup='issue' génère le paramètre 'issue_pk'
routers.NestedDefaultRouter(router, r'projects', lookup='project')
```

### **basename**
```python
# Nom unique pour éviter les conflits
projects_router.register(r'issues', IssueViewSet, basename='project-issues')
# Différent de :
router.register(r'issues', IssueViewSet, basename='issues')
```

## 💡 **Bonnes pratiques**

### ✅ **À faire**
```python
# 1. Noms cohérents pour lookup
lookup='project'  # → project_pk dans les kwargs

# 2. Basename descriptifs
basename='project-issues'  # Évite les conflits

# 3. Filtrage dans get_queryset()
def get_queryset(self):
    project_pk = self.kwargs['project_pk']
    return Issue.objects.filter(project_id=project_pk)

# 4. Validation des permissions par contexte
def get_object(self):
    obj = super().get_object()
    project_pk = self.kwargs['project_pk']
    if obj.project_id != int(project_pk):
        raise Http404
    return obj
```

### ❌ **À éviter**
```python
# 1. Trop d'imbrication (max 2-3 niveaux)
/api/projects/1/issues/2/comments/3/attachments/4/  # Trop profond

# 2. Oublier le filtrage
def get_queryset(self):
    return Issue.objects.all()  # ❌ Renvoie TOUTES les issues

# 3. Basename identiques
basename='issues'  # ❌ Conflit avec autres routes
```

## 🔍 **Débogage**

### **Voir toutes les routes générées**
```bash
# Commande Django pour lister les URLs
poetry run python manage.py show_urls
```

### **Tester une route imbriquée**
```bash
# Test avec curl
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/1/issues/

# Test dans le navigateur DRF
http://127.0.0.1:8000/api/projects/1/issues/
```

## 🎯 **Cas d'usage typiques**

### **E-commerce**
```python
/api/categories/1/products/           # Produits d'une catégorie
/api/orders/1/items/                  # Articles d'une commande
```

### **Blog**
```python
/api/blogs/1/posts/                   # Articles d'un blog
/api/posts/1/comments/                # Commentaires d'un article
```

### **Gestion de projets (SoftDesk)**
```python
/api/projects/1/contributors/         # Équipe d'un projet
/api/projects/1/issues/               # Tickets d'un projet
/api/projects/1/issues/5/comments/    # Commentaires d'un ticket
```

## 🏆 **Avantages**

1. **Sécurité automatique** : Filtrage par contexte
2. **URLs expressives** : Relations claires
3. **Code maintenable** : Logique métier respectée
4. **Performance** : Requêtes optimisées
5. **Standards REST** : Architecture conforme

---

**💡 Conseil :** `NestedDefaultRouter` est parfait pour modéliser des relations parent-enfant claires. Utilisez-le quand vos ressources ont une hiérarchie naturelle !
