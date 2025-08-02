# 📁 Endpoints Projets

[← Retour à la documentation API](./README.md)

## 📋 Vue d'ensemble

Les projets sont le cœur de l'application. Un utilisateur peut créer des projets, en devenir automatiquement l'auteur et le premier contributeur.

## 🔗 Endpoints

### Liste des projets

```http
GET /api/projects/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Application Mobile",
            "type": "iOS",
            "author_username": "john_doe",
            "contributors_count": 3,
            "created_time": "2024-01-15T10:30:00Z"
        }
    ]
}
```

**Note** : Affiche uniquement les projets où l'utilisateur est contributeur.

### Créer un projet

```http
POST /api/projects/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nouvelle Application",
    "description": "Une application révolutionnaire",
    "type": "back-end"
}
```

**Réponse (201 Created)** :
```json
{
    "id": 2,
    "name": "Nouvelle Application",
    "description": "Une application révolutionnaire",
    "type": "back-end",
    "author": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    },
    "contributors": [
        {
            "user": {
                "id": 1,
                "username": "john_doe"
            },
            "created_time": "2024-01-15T14:00:00Z"
        }
    ],
    "created_time": "2024-01-15T14:00:00Z"
}
```

**Types disponibles** :
- `back-end`
- `front-end`
- `iOS`
- `Android`

### Détails d'un projet

```http
GET /api/projects/{id}/
Authorization: Bearer <token>
```

**Réponse complète avec contributeurs**.

### Modifier un projet

```http
PUT /api/projects/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nouveau nom",
    "description": "Nouvelle description"
}
```

**Permissions** : Auteur uniquement

### Supprimer un projet

```http
DELETE /api/projects/{id}/
Authorization: Bearer <token>
```

**Permissions** : Auteur uniquement
**Impact** : Supprime aussi toutes les issues et commentaires

### Ajouter un contributeur

```http
POST /api/projects/{id}/add-contributor/
Authorization: Bearer <token>
Content-Type: application/json

{
    "user_id": 3
}
```

**Réponse (201 Created)** :
```json
{
    "message": "Contributeur alice (ID: 3) ajouté"
}
```

**Permissions** : Auteur uniquement

### Liste des contributeurs

```http
GET /api/projects/{id}/contributors/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
[
    {
        "user": {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        },
        "created_time": "2024-01-15T10:30:00Z"
    }
]
```

## 📊 Formats de données

### ProjectList (résumé)
```json
{
    "id": 1,
    "name": "Mon Projet",
    "type": "back-end",
    "author_username": "john_doe",
    "contributors_count": 5,
    "created_time": "2024-01-15T10:30:00Z"
}
```

### ProjectDetail (complet)
```json
{
    "id": 1,
    "name": "Mon Projet",
    "description": "Description complète du projet",
    "type": "back-end",
    "author": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    },
    "contributors": [...],
    "created_time": "2024-01-15T10:30:00Z"
}
```

## ⚠️ Erreurs courantes

### Type invalide
```json
{
    "type": ["Type invalide. Choisir parmi: ['back-end', 'front-end', 'iOS', 'Android']"]
}
```

### Contributeur déjà ajouté
```json
{
    "error": "Déjà contributeur"
}
```

### Modification non autorisée
```json
{
    "detail": "Seul l'auteur peut modifier le projet"
}
```

## 🔒 Permissions

| Action | Contributeur | Auteur | Autres |
|--------|--------------|--------|--------|
| Voir liste | ✅ | ✅ | ❌ |
| Voir détails | ✅ | ✅ | ❌ |
| Créer | ✅ | ✅ | ✅ |
| Modifier | ❌ | ✅ | ❌ |
| Supprimer | ❌ | ✅ | ❌ |
| Ajouter contributeur | ❌ | ✅ | ❌ |

## 📝 Notes

- L'auteur devient automatiquement contributeur à la création
- Seuls les projets où l'utilisateur est contributeur sont visibles
- La suppression est en CASCADE (issues et commentaires supprimés)
