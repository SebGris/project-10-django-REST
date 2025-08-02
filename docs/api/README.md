# 📊 Documentation API SoftDesk

[← Retour à la documentation](../README.md)

## 🎯 Vue d'ensemble

L'API SoftDesk est une API RESTful qui permet de gérer des projets, des issues et des commentaires. Elle utilise l'authentification JWT et suit les principes REST.

## 📚 Endpoints disponibles

### 🔐 [Authentification](./authentification.md)
- `POST /api/token/` - Obtenir un token d'accès
- `POST /api/token/refresh/` - Rafraîchir le token

### 👤 [Utilisateurs](./utilisateurs.md)
- `POST /api/users/` - Créer un compte
- `GET /api/users/` - Liste des utilisateurs
- `GET /api/users/{id}/` - Détails d'un utilisateur
- `PUT /api/users/{id}/` - Modifier son profil
- `DELETE /api/users/{id}/` - Supprimer son compte

### 📁 [Projets](./projets.md)
- `GET /api/projects/` - Liste des projets
- `POST /api/projects/` - Créer un projet
- `GET /api/projects/{id}/` - Détails d'un projet
- `PUT /api/projects/{id}/` - Modifier un projet
- `DELETE /api/projects/{id}/` - Supprimer un projet
- `POST /api/projects/{id}/add-contributor/` - Ajouter un contributeur

### 🐛 [Issues](./issues.md)
- `GET /api/projects/{project_id}/issues/` - Issues d'un projet
- `POST /api/projects/{project_id}/issues/` - Créer une issue
- `GET /api/projects/{project_id}/issues/{id}/` - Détails d'une issue
- `PUT /api/projects/{project_id}/issues/{id}/` - Modifier une issue
- `DELETE /api/projects/{project_id}/issues/{id}/` - Supprimer une issue

### 💬 [Commentaires](./commentaires.md)
- `GET /api/projects/{project_id}/issues/{issue_id}/comments/` - Commentaires d'une issue
- `POST /api/projects/{project_id}/issues/{issue_id}/comments/` - Créer un commentaire
- `PUT /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Modifier
- `DELETE /api/projects/{project_id}/issues/{issue_id}/comments/{id}/` - Supprimer

## 🔑 Authentification

Toutes les requêtes (sauf création de compte et login) nécessitent un header d'authentification :

```http
Authorization: Bearer <access_token>
```

## 📋 Formats de réponse

### Succès
```json
{
    "id": 1,
    "name": "Mon projet",
    "description": "Description du projet",
    ...
}
```

### Erreur
```json
{
    "detail": "Message d'erreur explicite",
    "code": "error_code"
}
```

## 📄 Pagination

Les listes sont paginées par 20 éléments :

```json
{
    "count": 42,
    "next": "http://api/projects/?page=2",
    "previous": null,
    "results": [...]
}
```

## 🚦 Codes de statut HTTP

| Code | Signification |
|------|---------------|
| 200 | OK - Succès |
| 201 | Created - Ressource créée |
| 204 | No Content - Suppression réussie |
| 400 | Bad Request - Données invalides |
| 401 | Unauthorized - Non authentifié |
| 403 | Forbidden - Non autorisé |
| 404 | Not Found - Ressource introuvable |
| 500 | Server Error - Erreur serveur |

## 🧪 Tester l'API

- [Collection Postman](../tests/postman-collection.md)
- [Interface DRF](http://localhost:8000/api/)
- [Swagger/OpenAPI](./openapi-schema.json) (si configuré)
