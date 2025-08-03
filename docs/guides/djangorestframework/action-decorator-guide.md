# 🎯 Le décorateur @action dans Django REST Framework

[← Retour aux guides DRF](./README.md) | [Documentation officielle](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)

## 📋 Vue d'ensemble

Le décorateur `@action` est une fonctionnalité **spécifique à Django REST Framework** (pas disponible dans Django standard) qui permet d'ajouter des endpoints personnalisés à un ViewSet, au-delà des actions CRUD standard.

> ⚠️ **Important** : `@action` n'existe que dans Django REST Framework. Pour Django pur, vous devez créer des vues séparées avec des URLs distinctes.

## 🆚 Django vs Django REST Framework

### Django standard (sans DRF)
```python
# views.py - Django pur
def user_profile(request):
    # Logique de vue
    return render(request, 'profile.html')

# urls.py
urlpatterns = [
    path('users/profile/', user_profile, name='user-profile'),
]
```

### Django REST Framework
```python
# views.py - Avec DRF
class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        # URL automatiquement générée : /api/users/profile/
        return Response(serializer.data)
```

## 🔧 Syntaxe et paramètres

### Syntaxe de base

```python
@action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
def profile(self, request):
    # Votre logique ici
```

### Paramètres principaux

#### 1. **`detail`** (boolean)
- `detail=False` : Action sur la collection
  - URL générée : `/api/users/profile/`
  - Pas d'ID dans l'URL
  
- `detail=True` : Action sur une instance spécifique
  - URL générée : `/api/users/{id}/custom-action/`
  - Nécessite un ID

#### 2. **`methods`** (list)
Liste des méthodes HTTP acceptées :
```python
methods=['get']           # GET uniquement
methods=['post']          # POST uniquement
methods=['get', 'patch']  # GET et PATCH
methods=['get', 'post', 'put', 'delete']  # Toutes les méthodes
```

#### 3. **`permission_classes`** (list)
Permissions spécifiques pour cette action :
```python
permission_classes=[IsAuthenticated]  # Authentification requise
permission_classes=[AllowAny]         # Accès public
permission_classes=[IsOwner, IsAuthenticated]  # Permissions multiples
```

#### 4. **Paramètres optionnels**
- `url_path` : Personnaliser l'URL (par défaut : nom de la méthode)
- `url_name` : Nom pour reverse()
- `serializer_class` : Serializer spécifique pour cette action

## 💡 Exemples pratiques

### Action sur la collection (detail=False)

```python
class UserViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        """
        GET /api/users/profile/ - Consulter son profil
        PATCH /api/users/profile/ - Modifier son profil
        """
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
```

### Action sur une instance (detail=True)

```python
class ProjectViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """
        POST /api/projects/{id}/add-contributor/
        Ajoute un contributeur au projet
        """
        project = self.get_object()
        user_id = request.data.get('user_id')
        # Logique d'ajout du contributeur
        return Response({'status': 'contributor added'})
```

### Avec URL et serializer personnalisés

```python
class UserViewSet(viewsets.ModelViewSet):
    @action(
        detail=True,
        methods=['post'],
        permission_classes=[IsAuthenticated],
        serializer_class=PasswordChangeSerializer,
        url_path='change-password',
        url_name='user-change-password'
    )
    def change_password(self, request, pk=None):
        """
        POST /api/users/{id}/change-password/
        Utilise PasswordChangeSerializer au lieu du serializer par défaut
        """
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Logique de changement de mot de passe
        return Response({'status': 'password changed'})
```

## 🚀 Cas d'usage dans SoftDesk

### 1. Profil utilisateur (`/users/profile/`)

```python
@action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
def profile(self, request):
    """Endpoint personnel sans exposer l'ID utilisateur"""
    # Accessible via /api/users/profile/
    # Pas besoin de connaître son propre ID
```

### 2. Ajout de contributeur (`/projects/{id}/add-contributor/`)

```python
@action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsProjectAuthor])
def add_contributor(self, request, pk=None):
    """Action spécifique sur un projet"""
    # Seul l'auteur du projet peut ajouter des contributeurs
```

## ✅ Avantages

1. **RESTful** : Étend l'API tout en restant RESTful
2. **Flexible** : Permissions et serializers personnalisés par action
3. **Automatique** : Routes générées automatiquement par le router
4. **Organisé** : Garde la logique liée dans le même ViewSet
5. **DRY** : Évite la duplication de code

## ⚠️ Bonnes pratiques

### 1. Nommage cohérent
```python
# ✅ Bon : verbe_nom
@action(detail=True, methods=['post'])
def send_notification(self, request, pk=None):

# ❌ Éviter : nom seul
@action(detail=True, methods=['post'])
def notification(self, request, pk=None):
```

### 2. Documentation claire
```python
@action(detail=False, methods=['get'])
def statistics(self, request):
    """
    Récupère les statistiques globales.
    
    Permissions: Authentifié
    Retourne: Dict avec counts et moyennes
    """
```

### 3. Permissions appropriées
```python
# Action publique
@action(detail=False, methods=['get'], permission_classes=[AllowAny])
def public_stats(self, request):

# Action restreinte
@action(detail=True, methods=['delete'], permission_classes=[IsOwner])
def delete_sensitive_data(self, request, pk=None):
```

## 📊 Comparaison avec les vues standard

| Aspect | Vue standard | @action |
|--------|--------------|---------|
| URL | Fixe (`/users/`, `/users/{id}/`) | Personnalisable |
| Méthodes | CRUD standard | Librement définies |
| Permissions | Une par ViewSet | Une par action |
| Serializer | Un principal | Un par action possible |
| Flexibilité | Limitée | Totale |

## 🔗 URLs générées

Pour un `UserViewSet` avec router :

```python
# Actions standard (automatiques)
GET    /api/users/           # list
POST   /api/users/           # create
GET    /api/users/{id}/      # retrieve
PUT    /api/users/{id}/      # update
DELETE /api/users/{id}/      # destroy

# Actions personnalisées avec @action
GET    /api/users/profile/   # detail=False
PATCH  /api/users/profile/   # detail=False
POST   /api/users/{id}/set-password/  # detail=True
```

## 📚 Ressources

- [Documentation officielle DRF - ViewSet actions](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)
- [Guide des ViewSets](./modelviewset-guide.md)
- [Guide du DefaultRouter](./defaultrouter-guide.md)

## 💻 Code complet d'exemple

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Action collection : profil personnel
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Gère le profil de l'utilisateur connecté"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    # Action instance : activation de compte
    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def activate(self, request, pk=None):
        """Active un compte utilisateur"""
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'account activated'})
    
    # Action collection : statistiques
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def stats(self, request):
        """Retourne les statistiques utilisateurs"""
        return Response({
            'total_users': User.objects.count(),
            'active_users': User.objects.filter(is_active=True).count()
        })
```

Ce guide couvre tous les aspects du décorateur `@action`, de la syntaxe de base aux cas d'usage avancés, en passant par les bonnes pratiques et des exemples concrets du projet SoftDesk.
