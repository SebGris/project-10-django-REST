# 📖 API SoftDesk - Guide de Référence Complète

## 🌐 Vue d'ensemble

L'API SoftDesk est une API REST sécurisée pour la gestion de projets collaboratifs avec système de tickets (issues) et commentaires. Elle intègre une authentification JWT robuste et respecte la conformité RGPD.

**Base URL :** `http://127.0.0.1:8000/api/`

## 🔐 Authentification

### Obtenir un token JWT

**Endpoint :** `POST /api/token/`

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SoftDesk2025!"
  }'
```

**Réponse :**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Rafraîchir un token

**Endpoint :** `POST /api/token/refresh/`

```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Utiliser le token

Ajouter le header d'authentification à toutes les requêtes protégées :

```bash
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 👥 API Utilisateurs

### Inscription (publique)

**Endpoint :** `POST /api/users/`

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "SecurePass123!",
    "age": 25,
    "can_be_contacted": true,
    "can_data_be_shared": false
  }'
```

**Validation RGPD :** Les utilisateurs de moins de 15 ans sont rejetés.

### Lister les utilisateurs

**Endpoint :** `GET /api/users/`
**Auth :** Requis

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/
```

### Profil personnel

**Endpoint :** `GET /api/users/profile/`
**Auth :** Requis

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/profile/
```

### Modifier le profil

**Endpoint :** `PUT /api/users/profile/`
**Auth :** Requis

```bash
curl -X PUT http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "can_be_contacted": false
  }'
```

## 📋 API Projets

### Lister les projets

**Endpoint :** `GET /api/projects/`
**Auth :** Requis

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/
```

**Réponse :**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Projet Web",
      "description": "Application web moderne",
      "type": "front_end",
      "author": {
        "id": 1,
        "username": "admin"
      },
      "created_time": "2025-01-15T10:30:00Z"
    }
  ]
}
```

### Créer un projet

**Endpoint :** `POST /api/projects/`
**Auth :** Requis

```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nouveau Projet",
    "description": "Description du projet",
    "type": "back_end"
  }'
```

**Types de projets disponibles :**
- `back_end`
- `front_end`
- `ios`
- `android`

### Détails d'un projet

**Endpoint :** `GET /api/projects/{id}/`
**Auth :** Requis (contributeur)

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/1/
```

### Modifier un projet

**Endpoint :** `PUT /api/projects/{id}/`
**Auth :** Requis (auteur uniquement)

```bash
curl -X PUT http://127.0.0.1:8000/api/projects/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Nom modifié",
    "description": "Description mise à jour",
    "type": "front_end"
  }'
```

### Supprimer un projet

**Endpoint :** `DELETE /api/projects/{id}/`
**Auth :** Requis (auteur uniquement)

```bash
curl -X DELETE http://127.0.0.1:8000/api/projects/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Ajouter un contributeur

**Endpoint :** `POST /api/projects/{id}/add-contributor/`
**Auth :** Requis (auteur uniquement)

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/add-contributor/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 2}'
```

## 🐛 API Issues

### Lister les issues

**Endpoint :** `GET /api/issues/`
**Auth :** Requis

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/issues/
```

### Créer une issue

**Endpoint :** `POST /api/issues/`
**Auth :** Requis (contributeur du projet)

```bash
curl -X POST http://127.0.0.1:8000/api/issues/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bug critique",
    "description": "Description détaillée du bug",
    "tag": "bug",
    "priority": "high",
    "project": 1,
    "assigned_to": 2
  }'
```

**Tags disponibles :**
- `bug`
- `feature`
- `task`

**Priorités disponibles :**
- `low`
- `medium`
- `high`

**Statuts disponibles :**
- `to_do`
- `in_progress`
- `finished`

### Détails d'une issue

**Endpoint :** `GET /api/issues/{id}/`
**Auth :** Requis (contributeur du projet)

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/issues/1/
```

### Modifier une issue

**Endpoint :** `PUT /api/issues/{id}/`
**Auth :** Requis (auteur de l'issue)

```bash
curl -X PUT http://127.0.0.1:8000/api/issues/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Titre modifié",
    "status": "in_progress",
    "priority": "medium"
  }'
```

### Supprimer une issue

**Endpoint :** `DELETE /api/issues/{id}/`
**Auth :** Requis (auteur de l'issue)

```bash
curl -X DELETE http://127.0.0.1:8000/api/issues/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 💬 API Commentaires

### Lister les commentaires

**Endpoint :** `GET /api/comments/`
**Auth :** Requis

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/comments/
```

### Créer un commentaire

**Endpoint :** `POST /api/comments/`
**Auth :** Requis (contributeur du projet)

```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Commentaire détaillé sur cette issue",
    "issue": 1
  }'
```

### Détails d'un commentaire

**Endpoint :** `GET /api/comments/{id}/`
**Auth :** Requis (contributeur du projet)

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/comments/1/
```

### Modifier un commentaire

**Endpoint :** `PUT /api/comments/{id}/`
**Auth :** Requis (auteur du commentaire)

```bash
curl -X PUT http://127.0.0.1:8000/api/comments/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Commentaire mis à jour"
  }'
```

### Supprimer un commentaire

**Endpoint :** `DELETE /api/comments/{id}/`
**Auth :** Requis (auteur du commentaire)

```bash
curl -X DELETE http://127.0.0.1:8000/api/comments/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔗 Routes imbriquées (RESTful)

### Issues d'un projet

**Endpoint :** `GET /api/projects/{project_id}/issues/`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/1/issues/
```

### Créer une issue dans un projet

**Endpoint :** `POST /api/projects/{project_id}/issues/`

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Nouvelle issue",
    "description": "Description",
    "tag": "feature"
  }'
```

### Commentaires d'une issue

**Endpoint :** `GET /api/projects/{project_id}/issues/{issue_id}/comments/`

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/1/issues/1/comments/
```

### Créer un commentaire sur une issue

**Endpoint :** `POST /api/projects/{project_id}/issues/{issue_id}/comments/`

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/1/comments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Nouveau commentaire"
  }'
```

## 🔒 Permissions et sécurité

### Règles d'autorisation

#### Projets
- **Lecture :** Contributeurs du projet
- **Création :** Utilisateurs authentifiés
- **Modification :** Auteur du projet uniquement
- **Suppression :** Auteur du projet uniquement

#### Issues
- **Lecture :** Contributeurs du projet
- **Création :** Contributeurs du projet
- **Modification :** Auteur de l'issue
- **Suppression :** Auteur de l'issue

#### Commentaires
- **Lecture :** Contributeurs du projet
- **Création :** Contributeurs du projet
- **Modification :** Auteur du commentaire
- **Suppression :** Auteur du commentaire

### Codes d'erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Créé |
| 204 | Supprimé |
| 400 | Données invalides |
| 401 | Non authentifié |
| 403 | Non autorisé |
| 404 | Non trouvé |
| 429 | Trop de requêtes |

### Limitations (Throttling)

- **Utilisateurs anonymes :** 100 requêtes/heure
- **Utilisateurs authentifiés :** 1000 requêtes/heure

## 📊 Pagination

Toutes les listes sont paginées avec 20 éléments par page.

**Exemple de réponse paginée :**
```json
{
  "count": 45,
  "next": "http://127.0.0.1:8000/api/projects/?page=2",
  "previous": null,
  "results": [...]
}
```

**Navigation :**
- `?page=2` - Page suivante
- `?page_size=10` - Nombre d'éléments (max 100)

## 🧪 Tester l'API

### Avec Postman
1. Importer la collection : `docs/postman/SoftDesk_API_Collection.json`
2. Configurer l'environnement : `base_url = http://127.0.0.1:8000`
3. Exécuter les requêtes dans l'ordre

### Avec curl
Voir les exemples dans chaque section ci-dessus.

### Interface DRF
Accédez à `http://127.0.0.1:8000/api/` pour une interface graphique.

### Scripts automatiques
```bash
# Test complet de l'API
poetry run python tests/api/test_complete_api.py

# Test des routes imbriquées
poetry run python tests/api/test_nested_routes.py
```

## 🌱 Green Code

L'API est optimisée pour les performances et l'éco-conception :

- **Requêtes optimisées :** select_related/prefetch_related
- **Pagination :** Réduction du volume de données
- **Cache :** Headers de cache appropriés
- **Sérialisation efficace :** JSON minimaliste

## 📚 Ressources

- **Interface DRF :** http://127.0.0.1:8000/api/
- **Admin Django :** http://127.0.0.1:8000/admin/
- **Collection Postman :** `docs/postman/SoftDesk_API_Collection.json`
- **Documentation technique :** `docs/ARCHITECTURE.md`

Cette documentation fournit tous les éléments nécessaires pour intégrer et utiliser efficacement l'API SoftDesk.
