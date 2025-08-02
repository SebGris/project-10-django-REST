# 📚 Guide des ModelViewSet - Django REST Framework

[← Retour à la documentation](../../README.md) | [DefaultRouter Guide](./defaultrouter-guide.md) | [Routes imbriquées](./nested-router-guide.md)

Ce guide explique l'utilisation des `ModelViewSet` dans le projet SoftDesk API, avec des exemples concrets tirés de notre codebase.

## 🎯 Qu'est-ce qu'un ModelViewSet ?

Un `ModelViewSet` est une classe fournie par Django REST Framework qui combine automatiquement toutes les actions CRUD (Create, Read, Update, Delete) pour un modèle Django donné.

### Actions HTTP automatiques
| HTTP | URL | Action DRF | Description |
|------|-----|------------|-------------|
| `GET` | `/api/projects/` | `list()` | Liste tous les projets |
| `POST` | `/api/projects/` | `create()` | Crée un nouveau projet |
| `GET` | `/api/projects/1/` | `retrieve()` | Récupère le projet ID=1 |
| `PUT` | `/api/projects/1/` | `update()` | Met à jour complètement le projet |
| `PATCH` | `/api/projects/1/` | `partial_update()` | Met à jour partiellement le projet |
| `DELETE` | `/api/projects/1/` | `destroy()` | Supprime le projet |

## 🏗️ Anatomie d'un ModelViewSet

### Configuration de base
```python
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets
    """
    # 1. Serializer par défaut
    serializer_class = ProjectSerializer
    
    # 2. Permissions requises
    permission_classes = [permissions.IsAuthenticated]
    
    # 3. Données accessibles à l'utilisateur
    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(contributors__user=user) | models.Q(author=user)
        ).distinct()
```

## 🔧 Méthodes de personnalisation

### 1. Configuration dynamique

#### `get_queryset()` - Filtrer les données
```python
def get_queryset(self):
    """Retourner seulement les projets où l'utilisateur est contributeur ou auteur"""
    user = self.request.user
    # GREEN CODE: Optimiser les requêtes avec select_related et prefetch_related
    return Project.objects.filter(
        models.Q(contributors__user=user) | models.Q(author=user)
    ).select_related('author').prefetch_related(
        'contributors__user'  # Précharger les utilisateurs des contributeurs
    ).distinct()
```

#### `get_serializer_class()` - Choisir le serializer
```python
def get_serializer_class(self):
    """Utiliser un serializer différent pour la création/modification"""
    if self.action in ['create', 'update', 'partial_update']:
        return ProjectCreateUpdateSerializer  # Serializer simplifié
    return ProjectSerializer  # Serializer complet avec relations
```

### 2. Hooks d'action (perform_*)

Ces méthodes sont appelées automatiquement et permettent d'ajouter de la logique métier :

#### `perform_create()` - Logique lors de la création
```python
def perform_create(self, serializer):
    """Créer un projet - l'auteur sera automatiquement ajouté comme contributeur"""
    user = self.request.user
    serializer.save(author=user)
    # L'auteur est automatiquement ajouté comme contributeur via Project.save()
```

### 3. Surcharge complète des actions

Pour un contrôle total, vous pouvez surcharger les méthodes d'action :

#### `create()` - Contrôle total de la création
```python
def create(self, request, *args, **kwargs):
    """Créer un projet et retourner la réponse complète avec l'ID"""
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    
    # Retourner la réponse avec le ProjectSerializer complet (avec ID)
    instance = serializer.instance
    response_serializer = ProjectSerializer(instance, context={'request': request})
    headers = self.get_success_headers(response_serializer.data)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
```

## ✨ Actions personnalisées (@action)

Les actions personnalisées permettent d'ajouter des endpoints spécialisés :

### Action de détail (detail=True)
```python
@action(detail=True, methods=['post'], url_path='add-contributor')
def add_contributor(self, request, pk=None):
    """
    Ajouter un contributeur au projet
    URL générée: /api/projects/{id}/add-contributor/
    """
    project = self.get_object()  # Récupère le projet via pk
    
    # Vérifications de permissions
    if not project.can_user_modify(request.user):
        return Response(
            {"error": "Seul l'auteur peut ajouter des contributeurs"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Logique métier...
    username = request.data.get('username')
    user_to_add = User.objects.get(username=username)
    
    # Créer le contributeur
    contributor = Contributor.objects.create(user=user_to_add, project=project)
    serializer = ContributorSerializer(contributor)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
```

### Action de collection (detail=False)
```python
@action(detail=False, methods=['get'])
def my_projects(self, request):
    """
    Retourner les projets de l'utilisateur connecté
    URL générée: /api/projects/my-projects/
    """
    user = request.user
    projects = Project.objects.filter(author=user)
    serializer = self.get_serializer(projects, many=True)
    return Response(serializer.data)
```

## 🎨 Variantes de ViewSet dans le projet

### 1. ModelViewSet (CRUD complet)
```python
class ProjectViewSet(viewsets.ModelViewSet):
    """Toutes les actions CRUD + actions personnalisées"""
    # GET, POST, PUT, PATCH, DELETE + add-contributor, remove-contributor
```

### 2. ReadOnlyModelViewSet (Lecture seule)
```python
class ContributorViewSet(viewsets.ReadOnlyModelViewSet):
    """Lecture seule - GET uniquement"""
    # GET /api/contributors/ et GET /api/contributors/{id}/
    # Pas de POST, PUT, PATCH, DELETE
```

## 🔄 Support des routes imbriquées

Notre projet utilise des routes imbriquées pour organiser les ressources :

```python
def get_queryset(self):
    """Retourner les issues selon le contexte (imbriqué ou global)"""
    user = self.request.user
    project_id = self.kwargs.get('project_pk')  # Récupérer l'ID depuis l'URL
    
    if project_id:
        # Route imbriquée: /projects/{project_id}/issues/
        project = Project.objects.get(id=project_id)
        return project.issues.select_related('author', 'assigned_to', 'project').all()
    else:
        # Route directe: /issues/
        return Issue.objects.filter(
            models.Q(project__contributors__user=user) | models.Q(project__author=user)
        ).distinct()
```

## 📊 Optimisations Green Code

Nos ViewSets incluent des optimisations pour réduire l'impact environnemental :

### 1. Éviter les requêtes N+1
```python
def get_queryset(self):
    return Project.objects.filter(
        contributors__user=user
    ).select_related('author').prefetch_related(
        'contributors__user'  # Précharger les utilisateurs des contributeurs
    ).distinct()
```

### 2. Pagination optimisée
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,  # Taille de page optimisée pour les performances
}
```

### 3. Limitation du taux de requêtes
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour'  # Limite par utilisateur
    },
}
```

## 🚀 Avantages des ModelViewSet

### ✅ Moins de code
**Sans ModelViewSet (approche manuelle) :**
```python
class ProjectListCreateView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class ProjectDetailView(APIView):
    def get(self, request, pk):
        # Code pour récupérer un projet
    # ... et ainsi de suite pour PUT, PATCH, DELETE
```

**Avec ModelViewSet :**
```python
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # C'est tout ! Les 6 actions sont automatiquement créées
```

### ✅ Routage automatique
```python
# urls.py
router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
# Crée automatiquement toutes les URLs nécessaires :
# GET/POST /api/projects/
# GET/PUT/PATCH/DELETE /api/projects/{id}/
# POST /api/projects/{id}/add-contributor/
```

### ✅ Cohérence
- Gestion d'erreurs standardisée
- Format de réponse cohérent
- Conventions REST respectées

## 🎯 Cas d'usage dans SoftDesk

| ViewSet | Type | Usage |
|---------|------|--------|
| `ProjectViewSet` | `ModelViewSet` | CRUD complet + gestion des contributeurs |
| `ContributorViewSet` | `ReadOnlyModelViewSet` | Lecture seule des contributeurs |
| `IssueViewSet` | `ModelViewSet` | CRUD des issues + routes imbriquées |
| `CommentViewSet` | `ModelViewSet` | CRUD des commentaires + routes imbriquées |

## 💡 Bonnes pratiques

1. **Utilisez `get_queryset()`** pour filtrer les données selon l'utilisateur connecté
2. **Surchargez `perform_*`** pour la logique métier simple
3. **Surchargez les méthodes complètes** pour un contrôle total
4. **Utilisez `@action`** pour des endpoints personnalisés
5. **Gérez les permissions** avec `permission_classes` ou `get_permissions()`
6. **Optimisez les requêtes** avec `select_related()` et `prefetch_related()`
7. **Documentez vos actions personnalisées** dans les docstrings

## 🔍 Débogage

### Vérifier les URLs générées
```bash
poetry run python manage.py show_urls
```

### Tester une action
```python
# Dans un test ou shell Django
from issues.views import ProjectViewSet
from django.test import RequestFactory

factory = RequestFactory()
request = factory.get('/api/projects/')
view = ProjectViewSet()
view.action = 'list'
view.request = request
queryset = view.get_queryset()
print(queryset.query)  # Voir la requête SQL générée
```

---

**Les ModelViewSet sont l'épine dorsale de notre API REST, offrant une base solide et extensible pour toutes nos ressources !** 🚀
