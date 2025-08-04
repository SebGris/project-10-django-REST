# 📮 Guide : Tester les permissions de l'API avec Postman

## 🚀 Configuration initiale avec Postman

Postman est l'outil recommandé pour tester efficacement les permissions et accès de l'API SoftDesk.

### 1. Prérequis
- Serveur Django démarré : `poetry run python manage.py runserver`
- Collection Postman importée (voir [Guide Postman](../postman/postman-guide.md))
- Environnement "SoftDesk Local" sélectionné

### 2. Workflow de test recommandé

1. **Obtenir un token JWT** : Exécuter `🔐 Authentication > Obtenir Token JWT`
2. **Vérifier l'authentification** : Tester `👥 Users > Profil Personnel (GET)`
3. **Créer des ressources** : Projet → Issue → Comment
4. **Tester les permissions** : Modifier/supprimer avec différents utilisateurs

## 📊 Scénarios de test des permissions

### Test 1 : Accès sans authentification

1. **Désactiver temporairement le token** :
   - Dans l'onglet "Authorization" de la requête
   - Sélectionner "No Auth" au lieu de "Inherit auth from parent"

2. **Tester les endpoints publics vs protégés** :
   ```
   ✅ POST /api/users/          → 201 Created (inscription publique)
   ❌ GET  /api/projects/        → 401 Unauthorized
   ❌ GET  /api/users/profile/   → 401 Unauthorized
   ```

### Test 2 : Permissions selon le rôle

#### Étape 1 : Se connecter en tant qu'admin
```json
POST /api/token/
{
    "username": "admin",
    "password": "SoftDesk2025!"
}
```

#### Étape 2 : Créer un projet
```json
POST /api/projects/
{
    "name": "Projet Admin",
    "description": "Projet créé par admin",
    "type": "back-end"
}
// Notez l'ID du projet créé
```

#### Étape 3 : Changer d'utilisateur
```json
POST /api/token/
{
    "username": "john_doe_1754220224",
    "password": "SecurePass123!"
}
```

#### Étape 4 : Tester les permissions
```
❌ PUT    /api/projects/{id}/  → 403 Forbidden (pas l'auteur)
❌ DELETE /api/projects/{id}/  → 403 Forbidden (pas l'auteur)
✅ GET    /api/projects/{id}/  → 200 OK (lecture autorisée)
```

### Test 3 : Contributeurs

1. **En tant qu'auteur du projet** : Ajouter un contributeur
   ```json
   POST /api/projects/{id}/add_contributor/
   {
       "user_id": 2
   }
   ```

2. **En tant que contributeur** : Créer une issue
   ```json
   POST /api/projects/{id}/issues/
   {
       "name": "Issue du contributeur",
       "description": "Test des permissions contributeur",
       "tag": "BUG",
       "priority": "MEDIUM",
       "status": "To Do"
   }
   ```

## 🔢 Codes de réponse et leur signification

### Vue d'ensemble dans Postman

| Code | Couleur | Signification | Action corrective |
|------|---------|---------------|-------------------|
| **200** | 🟢 Vert | Lecture réussie | - |
| **201** | 🟢 Vert | Création réussie | - |
| **204** | 🟢 Vert | Suppression réussie | - |
| **400** | 🟠 Orange | Données invalides | Vérifier le body |
| **401** | 🔴 Rouge | Non authentifié | Obtenir un token |
| **403** | 🔴 Rouge | Pas autorisé | Changer d'utilisateur |
| **404** | 🔴 Rouge | Ressource introuvable | Vérifier l'ID |

### Exemples concrets dans Postman

#### ✅ Succès (200/201)
- **Body** : Contient les données de la ressource
- **Headers** : Token valide accepté
- **Tests** : Tous en vert

#### ❌ Erreur d'authentification (401)
```json
{
    "detail": "Authentication credentials were not provided."
}
// Solution : Exécuter "Obtenir Token JWT"
```

#### ❌ Erreur de permission (403)
```json
{
    "detail": "You do not have permission to perform this action."
}
// Solution : Vérifier que vous êtes l'auteur de la ressource
```

#### ❌ Erreur de validation (400)
```json
{
    "age": ["L'âge minimum requis est de 15 ans (conformité RGPD)."],
    "type": ["Type invalide. Choisir parmi: ['back-end', 'front-end', 'iOS', 'Android']"]
}
// Solution : Corriger les données dans le body
```

## 🎯 Collection Runner pour tests automatisés

### Exécuter tous les tests de permissions

1. **Ouvrir le Collection Runner** : Icône "Runner" en bas de Postman
2. **Sélectionner** :
   - Collection : "SoftDesk API - Tests Complets"
   - Environnement : "SoftDesk Local"
   - Dossier : "🔒 Tests de Permissions"
3. **Cliquer "Run"**

### Résultats attendus
```
✅ Obtenir Token JWT          → 200 OK
❌ Accès sans token (401)     → 401 Unauthorized (attendu)
❌ Token invalide (401)       → 401 Unauthorized (attendu)
✅ Créer Projet              → 201 Created
❌ Modifier projet d'autrui   → 403 Forbidden (attendu)
```

## 💡 Astuces Postman

### 1. Variables dynamiques
- `{{$timestamp}}` : Génère un timestamp unique
- `{{$randomInt}}` : Nombre aléatoire
- `{{$guid}}` : UUID unique

### 2. Visualiser les réponses
- **Pretty** : JSON formaté
- **Raw** : Réponse brute
- **Preview** : Rendu HTML (pour les erreurs)

### 3. Console Postman
- **View > Show Postman Console** : Debug détaillé
- Voir les headers envoyés/reçus
- Tracer les redirections

### 4. Tests conditionnels
```javascript
// Dans l'onglet "Tests"
if (pm.response.code === 403) {
    pm.test("Permission refusée comme attendu", () => {
        pm.expect(pm.response.json().detail).to.include("permission");
    });
}
```

## 🗺️ Référence rapide des endpoints

| Ressource | Endpoint | Permissions |
|-----------|----------|-------------|
| **Token** | `POST /api/token/` | Public |
| **Inscription** | `POST /api/users/` | Public |
| **Profil** | `GET/PUT/PATCH /api/users/profile/` | Authentifié (propriétaire) |
| **Projets** | `GET /api/projects/` | Authentifié |
| **Projet** | `PUT/DELETE /api/projects/{id}/` | Auteur uniquement |
| **Contributeur** | `POST /api/projects/{id}/add_contributor/` | Auteur du projet |
| **Issues** | `POST /api/projects/{id}/issues/` | Contributeur du projet |
| **Comments** | `POST /api/projects/{id}/issues/{id}/comments/` | Contributeur du projet |

---

**Note** : Pour une documentation complète de la collection Postman, consultez le [Guide Postman](../postman/postman-guide.md).
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
