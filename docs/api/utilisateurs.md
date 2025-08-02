# 👤 Endpoints Utilisateurs

[← Retour à la documentation API](./README.md)

## 📋 Vue d'ensemble

Gestion des comptes utilisateurs avec respect du RGPD. Les utilisateurs peuvent créer un compte, consulter les profils et modifier leur propre profil.

## 🔗 Endpoints

### Créer un compte

```http
POST /api/users/
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "MotDePasse123!",
    "password_confirm": "MotDePasse123!",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

**Réponse (201 Created)** :
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false,
    "created_time": "2024-01-15T10:30:00Z"
}
```

**Validations** :
- Username unique
- Email valide et unique
- Age minimum : 15 ans (RGPD)
- Mot de passe : minimum 8 caractères
- Les deux mots de passe doivent correspondre

### Liste des utilisateurs

```http
GET /api/users/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
{
    "count": 42,
    "next": "http://api/users/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "can_be_contacted": true,
            "can_data_be_shared": false
        },
        ...
    ]
}
```

### Détails d'un utilisateur

```http
GET /api/users/{id}/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false,
    "created_time": "2024-01-15T10:30:00Z"
}
```

### Modifier son profil

```http
PUT /api/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "email": "newemail@example.com",
    "first_name": "Johnny",
    "age": 26,
    "can_be_contacted": false
}
```

**Règles** :
- ✅ Peut modifier : son propre profil uniquement
- ❌ Ne peut pas modifier : username, created_time
- ❌ Ne peut pas modifier : les profils des autres

### Modifier le mot de passe

```http
PATCH /api/users/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "password": "NouveauMotDePasse123!"
}
```

### Supprimer son compte

```http
DELETE /api/users/{id}/
Authorization: Bearer <token>
```

**Réponse (204 No Content)**

**Règles** :
- Seul le propriétaire peut supprimer son compte
- Supprime aussi tous ses projets, issues et commentaires (CASCADE)

## 📊 Formats de données

### UserSummary (liste)
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "can_be_contacted": true,
    "can_data_be_shared": false
}
```

### UserDetail (détail)
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false,
    "created_time": "2024-01-15T10:30:00Z"
}
```

## ⚠️ Erreurs courantes

### Username déjà pris
```json
{
    "username": ["A user with that username already exists."]
}
```

### Age insuffisant
```json
{
    "age": ["Conformément au RGPD, l'inscription n'est autorisée qu'aux personnes âgées d'au moins 15 ans."]
}
```

### Modification non autorisée
```json
{
    "detail": "Vous ne pouvez modifier que votre propre profil."
}
```

## 🔒 Permissions

| Action | Non authentifié | Authentifié | Propriétaire |
|--------|----------------|-------------|--------------|
| Créer compte | ✅ | ✅ | - |
| Liste users | ❌ | ✅ | ✅ |
| Voir profil | ❌ | ✅ | ✅ |
| Modifier | ❌ | ❌ | ✅ |
| Supprimer | ❌ | ❌ | ✅ |

## 📝 Notes RGPD

- **Consentement explicite** : `can_be_contacted` et `can_data_be_shared`
- **Droit à l'oubli** : Suppression complète du compte possible
- **Portabilité** : Export des données via l'API
- **Age minimum** : 15 ans requis
