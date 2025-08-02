# 👥 Tests SoftDesk - Guide de Validation API Utilisateurs

[← Retour à la documentation](./README.md) | [API Guide](./api-guide.md) | [Tests complets](./api-testing-complete-guide.md)

## 📋 Navigation
- [Prérequis](#prérequis)
- [Endpoints utilisateurs](#endpoints-utilisateurs)
- [Tests d'authentification](#tests-dauthentification)
- [Tests RGPD](#tests-rgpd)
- [Dépannage](../support/troubleshooting.md)

## 🚀 Prérequis
1. Démarrer le serveur Django :
```bash
poetry run python manage.py runserver
```

2. Créer un superutilisateur pour les tests :
```bash
poetry run python manage.py createsuperuser
```

## 📊 Endpoints à tester (CRUD complet)

### 1. 🔐 **Authentification JWT**
**POST** `http://127.0.0.1:8000/api/token/`
```json
{
    "username": "admin",
    "password": "votre_password"
}
```
**Réponse attendue :**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 2. 📝 **CREATE - Inscription d'un nouvel utilisateur**
**POST** `http://127.0.0.1:8000/api/users/`
- **Headers :** Aucun (endpoint public)
- **Body :**
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

### 3. 📖 **READ - Lister les utilisateurs**
**GET** `http://127.0.0.1:8000/api/users/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Réponse :** Liste des utilisateurs (infos publiques seulement)

### 4. 👤 **READ - Détails d'un utilisateur**
**GET** `http://127.0.0.1:8000/api/users/{id}/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Réponse :** Informations publiques de l'utilisateur

### 5. 🔧 **READ - Profil personnel**
**GET** `http://127.0.0.1:8000/api/users/profile/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Réponse :** Toutes les informations de l'utilisateur connecté

### 6. ✏️ **UPDATE - Modifier son profil (PUT)**
**PUT** `http://127.0.0.1:8000/api/users/profile/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Body :**
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

### 7. ✏️ **UPDATE - Modifier partiellement son profil (PATCH)**
**PATCH** `http://127.0.0.1:8000/api/users/profile/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Body :**
```json
{
    "can_be_contacted": true,
    "age": 27
}
```

### 8. 🗑️ **DELETE - Supprimer un utilisateur**
**DELETE** `http://127.0.0.1:8000/api/users/{id}/`
- **Headers :** `Authorization: Bearer YOUR_ACCESS_TOKEN`
- **Note :** Seul l'utilisateur peut supprimer son propre compte

## 🔒 Scénarios de test des permissions

### Test 1 : Inscription sans authentification ✅
- Endpoint : `POST /api/users/`
- Attendu : Succès (201 Created)

### Test 2 : Accès à la liste avec authentification ✅
- Endpoint : `GET /api/users/`
- Attendu : Liste des utilisateurs (200 OK)

### Test 3 : Accès à la liste sans authentification ❌
- Endpoint : `GET /api/users/` (sans token)
- Attendu : Erreur 401 Unauthorized

### Test 4 : Modification de son propre profil ✅
- Endpoint : `PUT /api/users/profile/`
- Attendu : Succès (200 OK)

### Test 5 : Tentative de modification d'un autre utilisateur ❌
- Endpoint : `PUT /api/users/{autre_id}/`
- Attendu : Erreur 403 Forbidden

## 📋 Codes de statut attendus

| Action | Endpoint | Auth | Status | Description |
|--------|----------|------|--------|-------------|
| POST | `/api/users/` | Non | 201 | Utilisateur créé |
| GET | `/api/users/` | Oui | 200 | Liste récupérée |
| GET | `/api/users/{id}/` | Oui | 200 | Détails récupérés |
| GET | `/api/users/profile/` | Oui | 200 | Profil récupéré |
| PUT | `/api/users/profile/` | Oui | 200 | Profil modifié |
| PATCH | `/api/users/profile/` | Oui | 200 | Profil modifié |
| DELETE | `/api/users/{id}/` | Oui | 204 | Utilisateur supprimé |

## 🎯 Validation de l'implémentation

✅ **Critères de réussite :**
1. Inscription d'un nouvel utilisateur sans authentification
2. Authentification JWT fonctionnelle
3. Liste des utilisateurs accessible aux utilisateurs authentifiés
4. Gestion du profil personnel (lecture/modification)
5. Permissions correctement appliquées
6. Validation des données (âge minimum, mots de passe correspondants)
7. Champs RGPD présents et fonctionnels

## 🐛 Tests d'erreurs

### Données invalides
- Âge < 15 ans → Erreur validation
- Mots de passe différents → Erreur validation
- Username déjà existant → Erreur conflit

### Permissions
- Accès sans token → 401 Unauthorized
- Modification d'un autre utilisateur → 403 Forbidden

## 🔧 Commandes utiles

```bash
# Démarrer le serveur
poetry run python manage.py runserver

# Créer un superutilisateur
poetry run python manage.py createsuperuser

# Accès interface admin
http://127.0.0.1:8000/admin/

# Interface DRF navigable
http://127.0.0.1:8000/api/users/
```
