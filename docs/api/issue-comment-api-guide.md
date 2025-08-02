# 🐛 Guide API Issues & Comments

[← Retour à la documentation](./README.md) | [API Guide](./api-guide.md) | [Architecture](../architecture/architecture.md)

## 📋 Navigation rapide
- [Vue d'ensemble](#vue-densemble)
- [Endpoints Issues](#endpoints-issues)
- [Endpoints Comments](#endpoints-comments)
- [Relations et permissions](#relations-et-permissions)
- [Tests avec Postman](../postman/postman-guide.md)

## 🎯 Vue d'ensemble

Cette documentation a pour but de tester l'API Django REST liée aux issues et commentaires d'un projet.

## 📋 Prérequis
- Serveur Django démarré : `poetry run python manage.py runserver`
- Superutilisateur créé : `poetry run python create_superuser.py`

## 🔐 1. Authentification
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}'
```

**Réponse attendue :**
```json
{
  "access": "eyJ0eXAiOiJKV1Q...",
  "refresh": "eyJ0eXAiOiJKV1Q..."
}
```

## 📋 2. Créer un projet (requis pour les issues)
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Projet Test Issues",
    "description": "Projet pour tester les issues et commentaires",
    "type": "back-end"
  }'
```

**Réponse attendue :**
```json
{
  "id": 1,
  "name": "Projet Test Issues",
  "description": "Projet pour tester les issues et commentaires",
  "type": "back-end",
  "author": {...},
  "contributors": [...],
  "created_time": "2025-07-20T..."
}
```

## 🐛 3. Créer une issue
```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bug de connexion",
    "description": "Les utilisateurs ne peuvent pas se connecter",
    "priority": "HIGH",
    "tag": "BUG",
    "status": "To Do",
    "project": 1
  }'
```

**Réponse attendue :**
```json
{
  "id": 1,
  "name": "Bug de connexion",
  "description": "Les utilisateurs ne peuvent pas se connecter",
  "priority": "HIGH",
  "tag": "BUG",
  "status": "To Do",
  "project": 1,
  "author": {...},
  "assigned_to": null,
  "created_time": "2025-07-20T..."
}
```

## 💬 4. Créer un commentaire
```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/issues/1/comments/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "J ai reproduit le bug, il semble lié au JWT",
    "issue": 1
  }'
```

**Réponse attendue :**
```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "description": "J ai reproduit le bug, il semble lié au JWT",
  "issue": 1,
  "author": {...},
  "created_time": "2025-07-20T..."
}
```

## 📖 5. Lister les ressources

### Lister toutes les issues
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/issues/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Lister tous les commentaires
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/issues/1/comments/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Détails d'une issue spécifique
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/issues/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## ✏️ 6. Modifier une issue
```bash
curl -X PATCH http://127.0.0.1:8000/api/projects/1/issues/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress",
    "priority": "MEDIUM"
  }'
```

## ❌ 7. Supprimer un commentaire
```bash
curl -X DELETE http://127.0.0.1:8000/api/comments/COMMENT_UUID/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🔒 8. Test des permissions

### Tentative de modification par un non-contributeur (doit échouer)
1. Créer un autre utilisateur
2. Se connecter avec ce nouvel utilisateur
3. Essayer de modifier l'issue → Doit retourner **403 Forbidden**

## 🌐 9. Interface web
Accédez à http://127.0.0.1:8000/api/ pour utiliser l'interface Django REST Framework.

---

## ✅ Codes de statut attendus
- **200** : GET (lecture réussie)
- **201** : POST (création réussie)
- **204** : DELETE (suppression réussie)
- **403** : Forbidden (permissions insuffisantes)
- **404** : Not Found (ressource non trouvée)

## 🧪 Script automatique
Pour tester automatiquement tous les endpoints :
```bash
poetry run python test_issue_comment_api.py
```
