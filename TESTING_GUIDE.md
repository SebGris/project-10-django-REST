# Guide de test avec Postman

## 📋 Collection de tests pour l'API SoftDesk

### **Étape 1 : Obtenir un token JWT**

**POST** `http://127.0.0.1:8000/api/token/`

**Body (JSON):**
```json
{
    "username": "admin",
    "password": "SoftDesk2025!"
}
```

**Réponse attendue :**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### **Étape 2 : Configurer l'authentification**

Dans Postman, ajoutez dans **Headers** :
```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### **Étape 3 : Tester les endpoints des projets**

#### **Lister les projets**
**GET** `http://127.0.0.1:8000/api/projects/`

#### **Créer un projet**
**POST** `http://127.0.0.1:8000/api/projects/`

**Body (JSON):**
```json
{
    "name": "Mon Premier Projet",
    "description": "Description du projet de test",
    "type": "back-end"
}
```

#### **Détails d'un projet**
**GET** `http://127.0.0.1:8000/api/projects/1/`

#### **Modifier un projet**
**PUT** `http://127.0.0.1:8000/api/projects/1/`

**Body (JSON):**
```json
{
    "name": "Projet Modifié",
    "description": "Description mise à jour",
    "type": "front-end"
}
```

#### **Ajouter un contributeur**
**POST** `http://127.0.0.1:8000/api/projects/1/add-contributor/`

**Body (JSON):**
```json
{
    "username": "nom_utilisateur"
}
```

#### **Supprimer un projet**
**DELETE** `http://127.0.0.1:8000/api/projects/1/`

### **Codes de réponse attendus :**
- `200` : Succès (GET, PUT)
- `201` : Créé (POST)
- `204` : Supprimé (DELETE)
- `400` : Erreur de validation
- `401` : Non authentifié
- `403` : Non autorisé
- `404` : Non trouvé
