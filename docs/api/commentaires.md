# 💬 Endpoints Commentaires

[← Retour à la documentation API](./README.md)

## 📋 Vue d'ensemble

Les commentaires permettent aux contributeurs d'échanger sur les issues. Chaque commentaire est identifié par un UUID unique.

## 🔗 Endpoints

### Liste des commentaires d'une issue

```http
GET /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "description": "J'ai reproduit le bug sur iOS 17",
            "issue": 1,
            "author": {
                "id": 2,
                "username": "alice",
                "email": "alice@example.com"
            },
            "created_time": "2024-01-16T10:30:00Z"
        }
    ]
}
```

### Créer un commentaire

```http
POST /api/projects/{project_id}/issues/{issue_id}/comments/
Authorization: Bearer <token>
Content-Type: application/json

{
    "description": "Je confirme le bug, voici les logs..."
}
```

**Réponse (201 Created)** :
```json
{
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "description": "Je confirme le bug, voici les logs...",
    "issue": 1,
    "author": {
        "id": 3,
        "username": "bob",
        "email": "bob@example.com"
    },
    "created_time": "2024-01-16T11:00:00Z"
}
```

### Modifier un commentaire

```http
PUT /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "description": "EDIT: J'ai trouvé la solution, voir PR #42"
}
```

**Permissions** : Auteur du commentaire ou auteur du projet

### Supprimer un commentaire

```http
DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{comment_id}/
Authorization: Bearer <token>
```

**Permissions** : Auteur du commentaire ou auteur du projet

## 📊 Format de données

### Commentaire
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "description": "Contenu du commentaire",
    "issue": 1,
    "author": {
        "id": 2,
        "username": "alice",
        "email": "alice@example.com"
    },
    "created_time": "2024-01-16T10:30:00Z"
}
```

## 🔑 Particularités

### UUID comme identifiant
Les commentaires utilisent des UUID au lieu d'entiers :
- Format : `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- Meilleure distribution en base de données
- Évite les conflits d'ID
- Plus sécurisé (non prédictible)

### Exemple d'UUID
```
550e8400-e29b-41d4-a716-446655440000
123e4567-e89b-12d3-a456-426614174000
```

## ⚠️ Erreurs courantes

### Issue non trouvée
```json
{
    "detail": "Issue non trouvée"
}
```

### Commentaire vide
```json
{
    "description": ["Ce champ ne peut être vide."]
}
```

### UUID invalide
```json
{
    "detail": "UUID invalide"
}
```

## 🔒 Permissions

| Action | Contributeur | Auteur Comment | Auteur Projet | Autres |
|--------|--------------|----------------|---------------|--------|
| Voir liste | ✅ | ✅ | ✅ | ❌ |
| Créer | ✅ | - | ✅ | ❌ |
| Modifier | ❌ | ✅ | ✅ | ❌ |
| Supprimer | ❌ | ✅ | ✅ | ❌ |

## 📝 Workflow typique

1. **Contributeur** crée une issue
2. **Autres contributeurs** commentent
3. **Discussion** via commentaires
4. **Résolution** et fermeture de l'issue

## 🎯 Bonnes pratiques

1. **Commentaires constructifs** : Apporter de la valeur
2. **Édition** : Indiquer "EDIT:" lors des modifications
3. **Références** : Mentionner les PR, commits, etc.
4. **Formatage** : Utiliser Markdown si supporté

## 📌 Notes

- Les commentaires sont triés par date de création
- Pas de commentaires imbriqués (flat structure)
- L'auteur est automatiquement l'utilisateur connecté
- Pas de limite de longueur pour la description
