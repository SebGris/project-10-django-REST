# 🧪 Tests API Complète - Guide de Validation

[← Retour à la documentation](./README.md) | [Guide API](./api-guide.md) | [Guide de tests](../tests/testing-guide.md)

## 📋 Navigation rapide
- [Vue d'ensemble](#vue-densemble)
- [Installation et configuration](#installation-et-configuration)
- [Tests d'authentification](#tests-dauthentification)
- [Tests des endpoints](#tests-des-endpoints)
- [Tests de performance](#tests-de-performance)
- [Collection Postman](../postman/postman-guide.md)

## 🎯 Vue d'ensemble

Cette documentation a pour but de valider l'API complète de SoftDesk à travers une série de tests.

## 🚀 Étape 1 : Préparation

### Démarrer le serveur
```bash
cd "c:\Users\sebas\Documents\OpenClassrooms\Mes_projets\project-10-django-REST"
poetry run python manage.py runserver
```

Le serveur sera accessible à : `http://127.0.0.1:8000`

### Interface DRF navigable
Accédez à : `http://127.0.0.1:8000/api/` pour une interface graphique

## 🔐 Étape 2 : Authentification JWT

### 2.1 Obtenir un token d'accès
**POST** `http://127.0.0.1:8000/api/token/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "admin",
    "password": "SoftDesk2025!"
}
```

**Réponse attendue:**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

⚠️ **Important** : Copiez la valeur `access` pour l'utiliser dans les requêtes suivantes.

### 2.2 Rafraîchir un token
**POST** `http://127.0.0.1:8000/api/token/refresh/`

**Body (JSON):**
```json
{
    "refresh": "YOUR_REFRESH_TOKEN"
}
```

## 👥 Étape 3 : Tests des endpoints Users

### 3.1 📝 Inscription d'un nouvel utilisateur (PUBLIC)
**POST** `http://127.0.0.1:8000/api/users/`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false,
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!"
}
```

**Statut attendu:** `201 Created`

**🔐 VALIDATION RGPD :**
⚠️ **Important** : Les utilisateurs de moins de 15 ans ne peuvent pas s'inscrire (conformité RGPD).

**Test d'âge invalide (doit retourner 400):**
```json
{
    "username": "enfant",
    "email": "enfant@example.com", 
    "age": 12,
    "password": "TestPass123!",
    "password_confirm": "TestPass123!"
}
```

### 3.2 📖 Lister tous les utilisateurs (AUTHENTIFIÉ)
**GET** `http://127.0.0.1:8000/api/users/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Réponse:** Liste des utilisateurs (infos publiques uniquement)

### 3.3 👤 Voir les détails d'un utilisateur
**GET** `http://127.0.0.1:8000/api/users/{user_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**🔒 Permissions :**
- **Utilisateurs normaux** : Informations publiques uniquement (id, username, first_name, last_name)
- **Administrateurs** : Profil complet avec tous les champs (email, age, can_be_contacted, etc.)

**Exemple pour voir l'utilisateur 4 :**
```
GET http://127.0.0.1:8000/api/users/4/
Authorization: Bearer ADMIN_TOKEN
```

### 3.4 🔍 Voir son propre profil complet
**GET** `http://127.0.0.1:8000/api/users/profile/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Réponse:** Toutes les informations de l'utilisateur connecté

### 3.5 ✏️ Modifier son profil (PUT - complet)
**PUT** `http://127.0.0.1:8000/api/users/profile/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "john_doe_updated",
    "email": "john.updated@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 26,
    "can_be_contacted": false,
    "can_data_be_shared": true
}
```

**⚠️ Important :** Cet endpoint modifie TOUJOURS le profil de l'utilisateur connecté, peu importe le token utilisé.

### 3.5b ✏️ Modifier un utilisateur spécifique (Admin uniquement)
**PUT** `http://127.0.0.1:8000/api/users/{user_id}/`

**Headers:**
```
Authorization: Bearer ADMIN_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "username": "john_doe_updated",
    "email": "john.updated@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 26,
    "can_be_contacted": false,
    "can_data_be_shared": true
}
```

**⚠️ Important :** Seuls les superusers peuvent modifier d'autres utilisateurs via cet endpoint.

### 3.6 ✏️ Modifier partiellement son profil (PATCH)
**PATCH** `http://127.0.0.1:8000/api/users/profile/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "can_be_contacted": true,
    "age": 27
}
```

### 3.7 🗑️ Supprimer son compte
**DELETE** `http://127.0.0.1:8000/api/users/{user_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Note:** Un utilisateur ne peut supprimer que son propre compte.

## 📋 Étape 4 : Tests des endpoints Projects

### 4.1 📝 Créer un nouveau projet
**POST** `http://127.0.0.1:8000/api/projects/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "name": "Mon Premier Projet",
    "description": "Description détaillée du projet",
    "type": "back-end"
}
```

**Types disponibles:** `back-end`, `front-end`, `iOS`, `Android`

### 4.2 📖 Lister tous les projets
**GET** `http://127.0.0.1:8000/api/projects/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4.3 👁️ Voir les détails d'un projet
**GET** `http://127.0.0.1:8000/api/projects/{project_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4.4 ✏️ Modifier un projet (auteur uniquement)
**PUT** `http://127.0.0.1:8000/api/projects/{project_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "name": "Projet Modifié",
    "description": "Nouvelle description",
    "type": "front-end"
}
```

### 4.5 🗑️ Supprimer un projet (auteur uniquement)
**DELETE** `http://127.0.0.1:8000/api/projects/{project_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4.6 👥 Ajouter un contributeur à un projet
**POST** `http://127.0.0.1:8000/api/projects/{project_id}/add-contributor/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

**Body (JSON):**
```json
{
    "user_id": 2
}
```

### 4.7 📋 Voir les contributeurs d'un projet
**GET** `http://127.0.0.1:8000/api/projects/{project_id}/contributors/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 4.8 ❌ Supprimer un contributeur (auteur uniquement)
**DELETE** `http://127.0.0.1:8000/api/projects/{project_id}/contributors/{user_id}/`

**Headers:**
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🎯 Étape 5 : Scénarios de test complets

### Scénario 1 : Création complète d'un projet avec contributeurs

1. **S'authentifier** (obtenir le token)
2. **Créer un utilisateur** (inscription)
3. **S'authentifier avec le nouvel utilisateur**
4. **Créer un projet**
5. **Ajouter des contributeurs**
6. **Modifier le projet**
7. **Lister tous les projets**

### Scénario 2 : Test des permissions

1. **Créer un projet avec l'utilisateur A**
2. **S'authentifier avec l'utilisateur B**
3. **Essayer de modifier le projet** → Doit échouer (403 Forbidden)
4. **S'authentifier avec l'utilisateur A**
5. **Modifier le projet** → Doit réussir

## 🚨 Codes de statut HTTP attendus

| Action | Succès | Erreur Auth | Erreur Permission | Erreur Validation |
|--------|--------|-------------|-------------------|-------------------|
| POST users/ | 201 | - | - | 400 |
| GET users/ | 200 | 401 | - | - |
| GET users/profile/ | 200 | 401 | - | - |
| PUT users/profile/ | 200 | 401 | - | 400 |
| POST projects/ | 201 | 401 | - | 400 |
| GET projects/ | 200 | 401 | - | - |
| PUT projects/{id}/ | 200 | 401 | 403 | 400 |
| DELETE projects/{id}/ | 204 | 401 | 403 | - |

## 🛠️ Outils recommandés

### Postman
1. Créer une collection "SoftDesk API"
2. Configurer une variable d'environnement `{{token}}`
3. Utiliser les scripts de test automatiques

### cURL (Terminal)
```bash
# Obtenir un token
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}'

# Utiliser le token
curl -X GET http://127.0.0.1:8000/api/users/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Interface DRF (Navigateur)
Accédez à `http://127.0.0.1:8000/api/` pour une interface graphique interactive.

## 🔍 Validation des tests

### ✅ Critères de réussite

1. **Authentification JWT** fonctionne
2. **Inscription utilisateur** sans authentification
3. **CRUD utilisateurs** avec permissions correctes
4. **CRUD projets** avec permissions auteur
5. **Gestion des contributeurs** fonctionnelle
6. **Messages d'erreur** appropriés
7. **Validation des données** active

### 🐛 Tests d'erreurs à vérifier

1. **Token invalide/expiré** → 401 Unauthorized
2. **Modification par non-auteur** → 403 Forbidden
3. **Données invalides** → 400 Bad Request
4. **Ressource inexistante** → 404 Not Found

## 📊 Checklist de validation

- [ ] Obtention du token JWT
- [ ] Inscription d'un nouvel utilisateur
- [ ] Liste des utilisateurs (authentifié)
- [ ] Profil personnel (lecture/modification)
- [ ] Création d'un projet
- [ ] Liste des projets
- [ ] Modification d'un projet (auteur)
- [ ] Ajout de contributeurs
- [ ] Test des permissions (non-auteur)
- [ ] Suppression d'un projet (auteur)
- [ ] Messages d'erreur appropriés
