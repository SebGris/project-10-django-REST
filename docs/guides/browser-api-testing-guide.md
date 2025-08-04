# 🌐 Guide : Tester les permissions de l'API dans un navigateur

## 🚀 Interface Django REST Framework

Django REST Framework fournit une interface web interactive pour tester rapidement les permissions et accès de l'API SoftDesk directement dans un navigateur web.

### 1. Démarrer le serveur
```bash
poetry run python manage.py runserver
```

### 2. Accéder à l'interface
Ouvrez votre navigateur à : http://127.0.0.1:8000/api/

### 3. Tests de permissions sans authentification

1. **Accès public** :
   - ✅ http://127.0.0.1:8000/api/users/ (POST pour inscription)
   - ❌ http://127.0.0.1:8000/api/projects/ (401 Unauthorized)
   - ❌ http://127.0.0.1:8000/api/users/profile/ (401 Unauthorized)

2. **Observer les erreurs** :
   ```json
   {
       "detail": "Authentication credentials were not provided."
   }
   ```

### 4. S'authentifier via l'interface

1. Cliquez sur **"Log in"** en haut à droite
2. Entrez les identifiants :
   - Username: `admin`
   - Password: `SoftDesk2025!` (ou `SecurePass123!` pour les autres utilisateurs)
3. Une fois connecté, vous verrez "Log in" remplacé par votre username en haut à droite

**Note** : Si vous ne voyez pas votre username après connexion, cela peut être dû à :
- L'authentification par session n'est pas activée
- Vous utilisez uniquement JWT (sans sessions)

Pour vérifier votre connexion :
- Essayez d'accéder à http://127.0.0.1:8000/api/users/profile/
- Si vous êtes connecté, vous verrez vos informations
- Sinon, vous aurez une erreur 401

### 5. Tester les permissions authentifié

#### ✅ Lecture autorisée :
- http://127.0.0.1:8000/api/projects/
- http://127.0.0.1:8000/api/projects/1/
- http://127.0.0.1:8000/api/projects/1/issues/

#### ❌ Modification non autorisée (si pas auteur) :
1. Allez sur un projet dont vous n'êtes pas l'auteur
2. Essayez de le modifier via le formulaire
3. Vous obtiendrez : `"detail": "You do not have permission to perform this action."`

## 📊 Scénarios de test des permissions

### Test 1 : Création de projet
1. **Connecté** : POST sur http://127.0.0.1:8000/api/projects/
   - ✅ Formulaire de création disponible
   - ✅ Projet créé avec vous comme auteur

### Test 2 : Modification d'un projet
1. **Votre projet** : PUT sur http://127.0.0.1:8000/api/projects/1/
   - ✅ Formulaire de modification disponible
   
2. **Projet d'un autre** : PUT sur http://127.0.0.1:8000/api/projects/2/
   - ❌ Erreur 403 Forbidden

### Test 3 : Ajout de contributeur
1. **Votre projet** : POST sur http://127.0.0.1:8000/api/projects/1/add_contributor/
   ```json
   {"user_id": 2}
   ```
   - ✅ Contributeur ajouté

2. **Projet d'un autre** : 
   - ❌ Erreur 403 Forbidden

## 🎨 Console du navigateur (DevTools)

### Tests avec JavaScript
Ouvrez la console (F12) et testez :

```javascript
// Test sans authentification
fetch('http://127.0.0.1:8000/api/projects/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erreur:', error));

// Test avec token
const token = 'votre_token_ici';
fetch('http://127.0.0.1:8000/api/projects/', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data));

// Test de création
fetch('http://127.0.0.1:8000/api/projects/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Test Browser',
        description: 'Projet créé depuis le navigateur',
        type: 'back-end'
    })
})
.then(response => response.json())
.then(data => console.log('Projet créé:', data));
```

## 📋 Résumé des permissions

| Action | Non authentifié | Authentifié | Auteur | Admin |
|--------|----------------|-------------|---------|--------|
| Inscription | ✅ | ✅ | ✅ | ✅ |
| Voir projets | ❌ | ✅ | ✅ | ✅ |
| Créer projet | ❌ | ✅ | ✅ | ✅ |
| Modifier projet | ❌ | ❌ | ✅ | ✅ |
| Supprimer projet | ❌ | ❌ | ✅ | ✅ |
| Ajouter contributeur | ❌ | ❌ | ✅ | ✅ |

## 🔢 Codes de réponse HTTP de l'API

### ✅ Codes de succès (2xx)

| Code | Statut | Description | Exemple d'utilisation |
|------|--------|-------------|----------------------|
| **200** | OK | Requête réussie | GET sur une ressource existante |
| **201** | Created | Ressource créée avec succès | POST pour créer un projet/issue/comment |
| **204** | No Content | Suppression réussie | DELETE sur une ressource |

### ❌ Codes d'erreur client (4xx)

| Code | Statut | Description | Exemple de situation |
|------|--------|-------------|---------------------|
| **400** | Bad Request | Données invalides | Âge < 15 ans, mot de passe trop faible |
| **401** | Unauthorized | Non authentifié | Accès sans token JWT |
| **403** | Forbidden | Pas les permissions | Modifier un projet dont vous n'êtes pas l'auteur |
| **404** | Not Found | Ressource inexistante | Accès à un projet/issue/comment supprimé |
| **405** | Method Not Allowed | Méthode HTTP non autorisée | POST sur `/api/projects/1/` |

### 💥 Codes d'erreur serveur (5xx)

| Code | Statut | Description | Cause possible |
|------|--------|-------------|----------------|
| **500** | Internal Server Error | Erreur serveur | Bug dans le code |
| **503** | Service Unavailable | Service indisponible | Serveur en maintenance |

### 📊 Exemples concrets dans l'API SoftDesk

#### 1. **200 OK** - Lecture réussie
```http
GET /api/projects/1/
Authorization: Bearer {token}

Response: 200 OK
{
    "id": 1,
    "name": "Mon Projet",
    "description": "...",
    ...
}
```

#### 2. **201 Created** - Création réussie
```http
POST /api/projects/
Authorization: Bearer {token}
Content-Type: application/json

{
    "name": "Nouveau Projet",
    "description": "Description",
    "type": "back-end"
}

Response: 201 Created
{
    "id": 2,
    "name": "Nouveau Projet",
    ...
}
```

#### 3. **400 Bad Request** - Données invalides
```http
POST /api/users/
Content-Type: application/json

{
    "username": "jeune_user",
    "age": 12,  // ❌ Trop jeune
    ...
}

Response: 400 Bad Request
{
    "age": ["L'âge minimum requis est de 15 ans (conformité RGPD)."]
}
```

#### 4. **401 Unauthorized** - Non authentifié
```http
GET /api/projects/

Response: 401 Unauthorized
{
    "detail": "Authentication credentials were not provided."
}
```

#### 5. **403 Forbidden** - Pas les permissions
```http
DELETE /api/projects/1/  // Projet d'un autre utilisateur
Authorization: Bearer {token}

Response: 403 Forbidden
{
    "detail": "You do not have permission to perform this action."
}
```

#### 6. **404 Not Found** - Ressource inexistante
```http
GET /api/projects/999/
Authorization: Bearer {token}

Response: 404 Not Found
{
    "detail": "Not found."
}
```

### 🎯 Test rapide des codes HTTP

Dans la console du navigateur (F12) :

```javascript
// Fonction pour tester différents scénarios
async function testHttpCodes(token) {
    // Test 401 - Sans authentification
    const test401 = await fetch('http://127.0.0.1:8000/api/projects/');
    console.log('Sans auth:', test401.status); // 401

    // Test 200 - Lecture autorisée
    const test200 = await fetch('http://127.0.0.1:8000/api/projects/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    console.log('Lecture:', test200.status); // 200

    // Test 404 - Ressource inexistante
    const test404 = await fetch('http://127.0.0.1:8000/api/projects/99999/', {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    console.log('Inexistant:', test404.status); // 404

    // Test 400 - Données invalides
    const test400 = await fetch('http://127.0.0.1:8000/api/projects/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: '', // Nom vide
            type: 'invalid-type' // Type invalide
        })
    });
    console.log('Données invalides:', test400.status); // 400
}

// Utilisation
testHttpCodes('votre_token_ici');
```

## 💡 Astuces

1. **Session persistante** : L'authentification via l'interface DRF utilise les sessions, donc vous restez connecté entre les pages.

2. **Format JSON** : Ajoutez `?format=json` à l'URL pour forcer le format JSON :
   - http://127.0.0.1:8000/api/projects/?format=json

3. **Debug** : Les erreurs de permission sont très explicites dans l'interface DRF.

4. **Logout** : Cliquez sur votre username puis "Log out" pour tester à nouveau sans authentification.

## 🗺️ Types d'endpoints dans le code Python

### ViewSets et leurs endpoints automatiques

L'API utilise des `ModelViewSet` de Django REST Framework qui génèrent automatiquement plusieurs endpoints :

#### 1. **UserViewSet** (`users/views.py`)
```python
class UserViewSet(viewsets.ModelViewSet):
    # Génère automatiquement :
    # GET    /api/users/           - Liste des utilisateurs
    # POST   /api/users/           - Inscription (création)
    # GET    /api/users/{id}/      - Détails d'un utilisateur
    # PUT    /api/users/{id}/      - Mise à jour complète
    # PATCH  /api/users/{id}/      - Mise à jour partielle
    # DELETE /api/users/{id}/      - Suppression
    
    # Action personnalisée :
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        # GET/PUT/PATCH /api/users/profile/ - Profil personnel
```

#### 2. **ProjectViewSet** (`issues/views.py`)
```python
class ProjectViewSet(viewsets.ModelViewSet):
    # Endpoints automatiques :
    # GET    /api/projects/        - Liste des projets
    # POST   /api/projects/        - Créer un projet
    # GET    /api/projects/{id}/   - Détails d'un projet
    # PUT    /api/projects/{id}/   - Modifier complètement
    # PATCH  /api/projects/{id}/   - Modifier partiellement
    # DELETE /api/projects/{id}/   - Supprimer
    
    # Action personnalisée :
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        # POST /api/projects/{id}/add_contributor/ - Ajouter contributeur
```

#### 3. **ContributorViewSet** (`issues/views.py`)
```python
class ContributorViewSet(viewsets.ReadOnlyModelViewSet):
    # ReadOnly = seulement GET :
    # GET /api/projects/{project_id}/contributors/      - Liste
    # GET /api/projects/{project_id}/contributors/{id}/ - Détails
```

#### 4. **IssueViewSet** (`issues/views.py`)
```python
class IssueViewSet(viewsets.ModelViewSet):
    # Routes imbriquées sous project :
    # GET    /api/projects/{project_id}/issues/        - Liste
    # POST   /api/projects/{project_id}/issues/        - Créer
    # GET    /api/projects/{project_id}/issues/{id}/   - Détails
    # PUT    /api/projects/{project_id}/issues/{id}/   - Modifier
    # PATCH  /api/projects/{project_id}/issues/{id}/   - Patch
    # DELETE /api/projects/{project_id}/issues/{id}/   - Supprimer
```

#### 5. **CommentViewSet** (`issues/views.py`)
```python
class CommentViewSet(viewsets.ModelViewSet):
    # Routes doublement imbriquées :
    # GET    /api/projects/{p_id}/issues/{i_id}/comments/      - Liste
    # POST   /api/projects/{p_id}/issues/{i_id}/comments/      - Créer
    # GET    /api/projects/{p_id}/issues/{i_id}/comments/{id}/ - Détails
    # PUT    /api/projects/{p_id}/issues/{i_id}/comments/{id}/ - Modifier
    # PATCH  /api/projects/{p_id}/issues/{i_id}/comments/{id}/ - Patch
    # DELETE /api/projects/{p_id}/issues/{i_id}/comments/{id}/ - Supprimer
```

### Endpoints JWT (SimpleJWT)

```python
# Dans softdesk_support/urls.py
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# POST /api/token/         - Obtenir access & refresh tokens
# POST /api/token/refresh/ - Rafraîchir le token
```

### Configuration des routes (`softdesk_support/urls.py`)

```python
# Router principal
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)

# Routes imbriquées avec drf-nested-routers
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

# Routes doublement imbriquées
issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')
```

### Résumé des patterns d'URL

| Pattern | Type | Description |
|---------|------|-------------|
| `/api/{resource}/` | Collection | Liste, création |
| `/api/{resource}/{id}/` | Instance | Détails, modification, suppression |
| `/api/{resource}/{id}/{action}/` | Action custom | Actions spéciales (@action) |
| `/api/{parent}/{p_id}/{child}/` | Nested collection | Ressources imbriquées |
| `/api/{parent}/{p_id}/{child}/{c_id}/` | Nested instance | Instance imbriquée |

### Méthodes HTTP par type de ViewSet

| ViewSet Type | GET | POST | PUT | PATCH | DELETE |
|--------------|-----|------|-----|-------|--------|
| **ModelViewSet** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ReadOnlyModelViewSet** | ✅ | ❌ | ❌ | ❌ | ❌ |
| **@action custom** | Selon `methods=[]` | | | | |

---

**Note** : L'interface web de Django REST Framework est l'outil le plus pratique pour tester rapidement les permissions sans outils externes.
