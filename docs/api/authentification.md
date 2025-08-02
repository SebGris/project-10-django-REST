# 🔐 Authentification API

[← Retour à la documentation API](./README.md)

## 📋 Vue d'ensemble

L'API SoftDesk utilise l'authentification JWT (JSON Web Token) pour sécuriser les endpoints. Après connexion, vous recevez deux tokens :
- **Access token** : Pour les requêtes API (durée de vie courte : 5 minutes)
- **Refresh token** : Pour renouveler l'access token (durée de vie : 1 jour)

## 🔑 Endpoints d'authentification

### Obtenir les tokens (Login)

```http
POST /api/token/
Content-Type: application/json

{
    "username": "john_doe",
    "password": "mot_de_passe_securise"
}
```

**Réponse réussie (200 OK)** :
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Erreurs possibles** :
- `401 Unauthorized` : Identifiants incorrects
- `400 Bad Request` : Données manquantes

### Rafraîchir le token

```http
POST /api/token/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Réponse réussie (200 OK)** :
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 📨 Utilisation des tokens

### Header d'autorisation

Pour toutes les requêtes authentifiées, ajoutez le header :

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Exemple complet

```javascript
// 1. Login
const loginResponse = await fetch('/api/token/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'john_doe',
        password: 'password123'
    })
});

const tokens = await loginResponse.json();

// 2. Utiliser l'access token
const projectsResponse = await fetch('/api/projects/', {
    headers: {
        'Authorization': `Bearer ${tokens.access}`
    }
});

// 3. Rafraîchir si nécessaire
const refreshResponse = await fetch('/api/token/refresh/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        refresh: tokens.refresh
    })
});
```

## ⏱️ Durée de vie des tokens

| Token | Durée | Usage |
|-------|-------|-------|
| Access | 5 minutes | Requêtes API |
| Refresh | 1 jour | Renouveler l'access token |

## 🔄 Stratégie de renouvellement

1. **Automatique** : Intercepter les erreurs 401 et rafraîchir automatiquement
2. **Préventif** : Rafraîchir avant expiration (ex: toutes les 4 minutes)
3. **Manuel** : Laisser l'utilisateur se reconnecter

## 🚫 Gestion des erreurs

### Token expiré
```json
{
    "detail": "Given token not valid for any token type",
    "code": "token_not_valid",
    "messages": [
        {
            "token_class": "AccessToken",
            "token_type": "access",
            "message": "Token is invalid or expired"
        }
    ]
}
```

### Token manquant
```json
{
    "detail": "Authentication credentials were not provided."
}
```

## 🔒 Bonnes pratiques

1. **Ne jamais stocker les tokens en clair** dans le localStorage
2. **Utiliser HTTPS** en production
3. **Implémenter un système de logout** qui invalide les tokens
4. **Gérer l'expiration** côté client
5. **Ne pas partager** les tokens entre utilisateurs

## 📝 Notes

- Les tokens JWT sont **stateless** : pas de session côté serveur
- La rotation des refresh tokens est activée pour plus de sécurité
- En développement, vous pouvez augmenter la durée de vie dans `settings.py`
