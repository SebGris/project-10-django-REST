# 🐛 Endpoints Issues

[← Retour à la documentation API](./README.md)

## 📋 Vue d'ensemble

Les issues représentent les problèmes, bugs ou fonctionnalités à développer dans un projet. Seuls les contributeurs d'un projet peuvent créer et voir les issues.

## 🔗 Endpoints

### Liste des issues d'un projet

```http
GET /api/projects/{project_id}/issues/
Authorization: Bearer <token>
```

**Réponse (200 OK)** :
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Bug authentification",
            "description": "L'utilisateur ne peut pas se connecter",
            "priority": "HIGH",
            "tag": "BUG",
            "status": "In Progress",
            "project": 1,
            "author": {
                "id": 2,
                "username": "alice",
                "email": "alice@example.com"
            },
            "assigned_to": {
                "id": 3,
                "username": "bob",
                "email": "bob@example.com"
            },
            "created_time": "2024-01-16T09:00:00Z"
        }
    ]
}
```

### Créer une issue

```http
POST /api/projects/{project_id}/issues/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Nouveau bug critique",
    "description": "Description détaillée du problème",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "To Do",
    "assigned_to_id": 3
}
```

**Réponse (201 Created)** : Issue complète créée

**Champs obligatoires** :
- `name` : Titre de l'issue
- `description` : Description détaillée
- `tag` : Type d'issue

**Champs optionnels** :
- `priority` : LOW (défaut), MEDIUM, HIGH
- `status` : To Do (défaut), In Progress, Finished
- `assigned_to_id` : ID d'un contributeur du projet

### Détails d'une issue

```http
GET /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <token>
```

### Modifier une issue

```http
PUT /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "Bug authentification - URGENT",
    "status": "In Progress",
    "assigned_to_id": 4
}
```

**Permissions** : Auteur de l'issue ou auteur du projet

### Assigner/Désassigner une issue

```http
PATCH /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "assigned_to_id": 5  // Assigner à l'utilisateur 5
}

// OU pour désassigner
{
    "assigned_to_id": null
}
```

### Supprimer une issue

```http
DELETE /api/projects/{project_id}/issues/{issue_id}/
Authorization: Bearer <token>
```

**Permissions** : Auteur de l'issue ou auteur du projet
**Impact** : Supprime aussi tous les commentaires associés

## 📊 Formats de données

### Issue complète
```json
{
    "id": 1,
    "name": "Titre de l'issue",
    "description": "Description complète",
    "priority": "HIGH",        // LOW, MEDIUM, HIGH
    "tag": "BUG",             // BUG, FEATURE, TASK
    "status": "In Progress",   // To Do, In Progress, Finished
    "project": 1,
    "author": {
        "id": 2,
        "username": "alice",
        "email": "alice@example.com"
    },
    "assigned_to": {
        "id": 3,
        "username": "bob",
        "email": "bob@example.com"
    },
    "created_time": "2024-01-16T09:00:00Z"
}
```

## 📈 Valeurs possibles

### Priorités
| Valeur | Description |
|--------|-------------|
| LOW | Priorité faible (défaut) |
| MEDIUM | Priorité moyenne |
| HIGH | Priorité haute |

### Tags
| Valeur | Description |
|--------|-------------|
| BUG | Problème à corriger |
| FEATURE | Nouvelle fonctionnalité |
| TASK | Tâche à réaliser |

### Statuts
| Valeur | Description |
|--------|-------------|
| To Do | À faire (défaut) |
| In Progress | En cours |
| Finished | Terminé |

## ⚠️ Erreurs courantes

### Projet non trouvé
```json
{
    "detail": "Projet non trouvé"
}
```

### Assignation invalide
```json
{
    "assigned_to_id": ["L'utilisateur assigné doit être contributeur du projet"]
}
```

### Modification non autorisée
```json
{
    "detail": "Non autorisé"
}
```

## 🔒 Permissions

| Action | Contributeur | Auteur Issue | Auteur Projet | Autres |
|--------|--------------|--------------|---------------|--------|
| Voir liste | ✅ | ✅ | ✅ | ❌ |
| Créer | ✅ | - | ✅ | ❌ |
| Voir détails | ✅ | ✅ | ✅ | ❌ |
| Modifier | ❌ | ✅ | ✅ | ❌ |
| Supprimer | ❌ | ✅ | ✅ | ❌ |
| Assigner | ❌ | ✅ | ✅ | ❌ |

## 📝 Notes

- Seuls les contributeurs du projet peuvent être assignés
- L'auteur de l'issue est automatiquement l'utilisateur connecté
- Les issues sont filtrées par projet dans l'URL
- La suppression est en CASCADE (commentaires supprimés)
