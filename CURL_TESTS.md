# Tests avec curl

## 1. Obtenir un token
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "SoftDesk2025!"
  }'
```

## 2. Stocker le token (remplacez YOUR_TOKEN)
```bash
export TOKEN="YOUR_ACCESS_TOKEN_HERE"
```

## 3. Lister les projets
```bash
curl -X GET http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer $TOKEN"
```

## 4. Créer un projet
```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Projet Test",
    "description": "Description du test",
    "type": "back-end"
  }'
```

## 5. Voir les détails d'un projet
```bash
curl -X GET http://127.0.0.1:8000/api/projects/1/ \
  -H "Authorization: Bearer $TOKEN"
```
