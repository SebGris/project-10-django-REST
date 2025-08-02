# 🛣️ DefaultRouter Django REST Framework - Guide Complet

[← Retour à la documentation](./README.md) | [Django Guide](../django/django-guide.md) | [API Guide](../../api/api-guide.md)

## 📋 Navigation
- [Qu'est-ce que DefaultRouter ?](#quest-ce-que-defaultrouter-)
- [Configuration dans SoftDesk](#configuration-dans-softdesk)
- [Routes générées automatiquement](#routes-générées-automatiquement)
- [Routes imbriquées](./nested-router-guide.md)
- [Raw strings expliquées](../django/raw-strings-guide.md)

## 🎯 Qu'est-ce que DefaultRouter ?

Le `DefaultRouter` est le **routeur automatique** de Django REST Framework qui génère automatiquement toutes les URLs REST pour vos ViewSets. C'est l'un des composants les plus puissants de DRF qui vous fait gagner énormément de temps !

**En une ligne de code**, il génère 6 endpoints REST complets avec toutes les opérations CRUD.

## 🚀 **Avant/Après : La magie du DefaultRouter**

### ❌ **AVANT** (Approche manuelle - Django classique)
```python
# urls.py - Méthode laborieuse
from django.urls import path
from . import views

urlpatterns = [
    # Pour les projets
    path('api/projects/', views.ProjectListView.as_view()),
    path('api/projects/create/', views.ProjectCreateView.as_view()),
    path('api/projects/<int:pk>/', views.ProjectDetailView.as_view()),
    path('api/projects/<int:pk>/update/', views.ProjectUpdateView.as_view()),
    path('api/projects/<int:pk>/delete/', views.ProjectDeleteView.as_view()),
    
    # Pour les utilisateurs
    path('api/users/', views.UserListView.as_view()),
    path('api/users/create/', views.UserCreateView.as_view()),
    path('api/users/<int:pk>/', views.UserDetailView.as_view()),
    path('api/users/<int:pk>/update/', views.UserUpdateView.as_view()),
    path('api/users/<int:pk>/delete/', views.UserDeleteView.as_view()),
    
    # Pour les issues
    path('api/issues/', views.IssueListView.as_view()),
    path('api/issues/create/', views.IssueCreateView.as_view()),
    path('api/issues/<int:pk>/', views.IssueDetailView.as_view()),
    # ... et ainsi de suite pour CHAQUE modèle ! 😰
]

# Résultat : 50+ lignes d'URLs répétitives !
```

### ✅ **APRÈS** (Avec DefaultRouter - DRF)
```python
# urls.py - Méthode DRF magique ✨
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from issues.views import ProjectViewSet, IssueViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'issues', IssueViewSet, basename='issue')

urlpatterns = [
    path('api/', include(router.urls)),
]

# Résultat : 6 lignes qui génèrent 18+ endpoints ! 🚀
```

## 🔄 **Ce que génère automatiquement DefaultRouter**

### **Une seule ligne :**
```python
router.register(r'projects', ProjectViewSet, basename='project')
```

### **Génère automatiquement :**

| HTTP Method | URL Pattern | ViewSet Method | Action | Description |
|-------------|-------------|----------------|---------|-------------|
| `GET` | `/api/projects/` | `list()` | **List** | 📋 Liste tous les projets |
| `POST` | `/api/projects/` | `create()` | **Create** | ➕ Crée un nouveau projet |
| `GET` | `/api/projects/{id}/` | `retrieve()` | **Read** | 👁️ Récupère un projet spécifique |
| `PUT` | `/api/projects/{id}/` | `update()` | **Update** | ✏️ Met à jour complètement |
| `PATCH` | `/api/projects/{id}/` | `partial_update()` | **Partial Update** | 🔧 Met à jour partiellement |
| `DELETE` | `/api/projects/{id}/` | `destroy()` | **Delete** | 🗑️ Supprime le projet |

### **URLs générées avec noms :**
```python
# Noms d'URLs automatiques (pour reverse())
'project-list'          # /api/projects/
'project-detail'        # /api/projects/{id}/
```

## 🏗️ **Architecture SoftDesk expliquée**

Votre fichier `urls.py` utilise une architecture à **3 niveaux** :

### **🥇 Niveau 1 : Routeur Principal**
```python
# Routeur principal
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
```

**Génère :**
```
GET/POST     /api/users/                    # Gestion utilisateurs
GET/PUT/PATCH/DELETE /api/users/{id}/

GET/POST     /api/projects/                 # Gestion projets  
GET/PUT/PATCH/DELETE /api/projects/{id}/
```

### **🥈 Niveau 2 : Routes Imbriquées (Projets)**
```python
# Routes imbriquées pour les projets
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')
```

**Génère :**
```
GET/POST     /api/projects/{project_pk}/contributors/
GET/PUT/PATCH/DELETE /api/projects/{project_pk}/contributors/{id}/

GET/POST     /api/projects/{project_pk}/issues/
GET/PUT/PATCH/DELETE /api/projects/{project_pk}/issues/{id}/
```

### **🥉 Niveau 3 : Routes Ultra-Imbriquées (Comments)**
```python
# Routes imbriquées pour les issues
issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')
```

**Génère :**
```
GET/POST     /api/projects/{project_pk}/issues/{issue_pk}/comments/
GET/PUT/PATCH/DELETE /api/projects/{project_pk}/issues/{issue_pk}/comments/{id}/
```

## 📊 **Tableau récapitulatif de TOUS vos endpoints**

### **👥 Users**
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/users/` | Liste tous les utilisateurs |
| `POST` | `/api/users/` | Crée un utilisateur |
| `GET` | `/api/users/{id}/` | Détail d'un utilisateur |
| `PUT/PATCH` | `/api/users/{id}/` | Modifie un utilisateur |
| `DELETE` | `/api/users/{id}/` | Supprime un utilisateur |

### **📁 Projects** 
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/projects/` | Liste tous les projets |
| `POST` | `/api/projects/` | Crée un projet |
| `GET` | `/api/projects/{id}/` | Détail d'un projet |
| `PUT/PATCH` | `/api/projects/{id}/` | Modifie un projet |
| `DELETE` | `/api/projects/{id}/` | Supprime un projet |

### **👨‍💻 Contributors**
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/projects/{project_id}/contributors/` | Liste les contributeurs d'un projet |
| `POST` | `/api/projects/{project_id}/contributors/` | Ajoute un contributeur |
| `GET` | `/api/projects/{project_id}/contributors/{id}/` | Détail d'un contributeur |
| `DELETE` | `/api/projects/{project_id}/contributors/{id}/` | Retire un contributeur |

### **🐛 Issues**
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/projects/{project_id}/issues/` | Liste les issues d'un projet |
| `POST` | `/api/projects/{project_id}/issues/` | Crée une issue |
| `GET` | `/api/projects/{project_id}/issues/{id}/` | Détail d'une issue |
| `PUT/PATCH` | `/api/projects/{project_id}/issues/{id}/` | Modifie une issue |
| `DELETE` | `/api/projects/{project_id}/issues/{id}/` | Supprime une issue |

### **💬 Comments**
| Method | URL | Description |
|--------|-----|-------------|
| `GET` | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Liste les commentaires |
| `POST` | `/api/projects/{project_id}/issues/{issue_id}/comments/` | Crée un commentaire |
| `GET` | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Détail d'un commentaire |
| `PUT/PATCH` | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Modifie un commentaire |
| `DELETE` | `/api/projects/{project_id}/issues/{issue_id}/comments/{id}/` | Supprime un commentaire |

## 🎛️ **Paramètres de register()**

```python
router.register(prefix, viewset, basename=None)
```

### **1. prefix** - Le préfixe URL
```python
router.register(r'projects', ProjectViewSet)     # → /api/projects/
router.register(r'users', UserViewSet)           # → /api/users/
router.register(r'my-custom-endpoint', MyViewSet) # → /api/my-custom-endpoint/
```

### **2. viewset** - La classe ViewSet
```python
from issues.views import ProjectViewSet
router.register(r'projects', ProjectViewSet)
```

### **3. basename** - Nom de base (optionnel mais recommandé)
```python
router.register(r'projects', ProjectViewSet, basename='project')

# Génère les noms d'URLs :
# 'project-list'     → reverse('project-list')
# 'project-detail'   → reverse('project-detail', args=[pk])
```

## 🌟 **Types de routeurs dans votre projet**

### **1. DefaultRouter** (routeur principal)
```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
```

**Caractéristiques :**
- ✅ Génère une **API Root** navigable
- ✅ Support des **formats** (.json, .api)
- ✅ **Interface web** automatique
- ✅ **Trailing slash** configurables

### **2. NestedDefaultRouter** (routes imbriquées)
```python
from rest_framework_nested import routers

projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
```

**Caractéristiques :**
- ✅ **URLs imbriquées** : `/projects/{id}/issues/`
- ✅ **Relations parent-enfant**
- ✅ **Filtrage automatique** par parent
- ✅ **RESTful** et sémantique

## 💡 **API Root automatique**

DefaultRouter génère automatiquement une **page d'accueil** pour votre API :

**GET** `http://127.0.0.1:8000/api/`

```json
{
    "users": "http://127.0.0.1:8000/api/users/",
    "projects": "http://127.0.0.1:8000/api/projects/"
}
```

**Interface web navigable :**
![DRF Browsable API](https://www.django-rest-framework.org/img/quickstart.png)

## 🛠️ **Customisation avancée**

### **URLs personnalisées avec @action**
```python
# Dans votre ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

class ProjectViewSet(viewsets.ModelViewSet):
    
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        # POST /api/projects/{id}/add_contributor/
        project = self.get_object()
        # Logique d'ajout de contributeur
        return Response({'status': 'contributor added'})
    
    @action(detail=False)
    def my_projects(self, request):
        # GET /api/projects/my_projects/
        # Logique pour les projets de l'utilisateur connecté
        return Response(projects_data)
```

### **Génère automatiquement :**
```
POST /api/projects/{id}/add_contributor/
GET  /api/projects/my_projects/
```

## 🎯 **Avantages du DefaultRouter**

### ✅ **Rapidité de développement**
- **1 ligne** = 6 endpoints complets
- **Convention over configuration**
- **Pas de répétition** de code

### ✅ **Cohérence**
- **Standards REST** respectés
- **Nommage uniforme**
- **Patterns prévisibles**

### ✅ **Maintenance**
- **Centralisation** des routes
- **Modifications faciles**
- **Évolution simple**

### ✅ **Documentation automatique**
- **Interface web** navigable
- **API Root** avec liens
- **Formats multiples** (JSON, API)

### ✅ **Performance**
- **URLs optimisées**
- **Gestion automatique** des permissions
- **Filtrage intelligent**

## 🔧 **Commandes pour tester vos routes**

### **Lister toutes les URLs générées :**
```bash
cd softdesk_support
python manage.py show_urls

# Ou utiliser django-extensions :
pip install django-extensions
python manage.py show_urls | grep api
```

### **Tester l'API Root :**
```bash
curl http://127.0.0.1:8000/api/
```

### **Tester un endpoint spécifique :**
```bash
# Liste des projets
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/api/projects/

# Projet spécifique
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/api/projects/1/

# Issues d'un projet
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://127.0.0.1:8000/api/projects/1/issues/
```

## 📈 **Évolution de votre architecture**

### **Ajouter un nouveau modèle :**
```python
# 1. Créer le ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 2. Ajouter UNE ligne au router
router.register(r'categories', CategoryViewSet, basename='category')

# 3. Résultat : 6 nouveaux endpoints automatiquement ! 🎉
```

### **Ajouter des routes imbriquées :**
```python
# Routes pour les tâches dans les projets
tasks_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
tasks_router.register(r'tasks', TaskViewSet, basename='project-tasks')

# Génère : /api/projects/{id}/tasks/
```

## 🎓 **Bonnes pratiques**

### ✅ **Nommage cohérent**
```python
# Utilisez des noms au pluriel
router.register(r'projects', ProjectViewSet)     # ✅ Bon
router.register(r'project', ProjectViewSet)      # ❌ Éviter

# Utilisez des basenames explicites
router.register(r'projects', ProjectViewSet, basename='project')  # ✅ Bon
router.register(r'projects', ProjectViewSet)                      # ⚠️ Fonctionne mais moins explicite
```

### ✅ **Organisation modulaire**
```python
# Gardez les routeurs séparés par domaine fonctionnel
users_router = DefaultRouter()
users_router.register(r'users', UserViewSet)

projects_router = DefaultRouter() 
projects_router.register(r'projects', ProjectViewSet)

# Puis combinez dans urls.py principal
```

### ✅ **Documentation des endpoints**
```python
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets.
    
    list: Retourne la liste des projets accessibles à l'utilisateur
    create: Crée un nouveau projet
    retrieve: Retourne les détails d'un projet spécifique
    update: Met à jour un projet existant
    destroy: Supprime un projet
    """
```

## 🔗 **Ressources pour approfondir**

- **[DRF Routers Documentation](https://www.django-rest-framework.org/api-guide/routers/)**
- **[DRF Nested Routers](https://github.com/alanjds/drf-nested-routers)**
- **[REST API Design Best Practices](https://restfulapi.net/)**

---

**🎯 Le DefaultRouter est la clé de voûte qui transforme votre code Django en API REST puissante et cohérente en quelques lignes !**
