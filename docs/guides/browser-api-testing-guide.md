# 🌐 Guide : Tester les permissions de l'API dans un navigateur

## 🎯 Objectif

Tester rapidement les permissions et accès de l'API SoftDesk directement dans un navigateur web.

## 🚀 Méthode 1 : Interface Django REST Framework (Recommandée)

Django REST Framework fournit une interface web interactive pour tester l'API.

### 1. Démarrer le serveur
```bash
poetry run python manage.py runserver
```

### 2. Accéder à l'interface
Ouvrez votre navigateur à : http://127.0.0.1:8000/api/

### 3. Tests de permissions sans authentification

1. **Accès public** :
   - ✅ http://127.0.0.1:8000/api/users/ (POST pour inscription)
   - ❌ http://127.0.0.1:8000/api/projects/ (401 Unauthorized)
   - ❌ http://127.0.0.1:8000/api/users/profile/ (401 Unauthorized)

2. **Observer les erreurs** :
   ```json
   {
       "detail": "Authentication credentials were not provided."
   }
   ```

### 4. S'authentifier via l'interface

1. Cliquez sur **"Log in"** en haut à droite
2. Entrez les identifiants :
   - Username: `admin`
   - Password: `SoftDesk2025!`
3. Une fois connecté, vous verrez "Log in" remplacé par votre username en haut à droite

**Note** : Si vous ne voyez pas votre username après connexion, cela peut être dû à :
- L'authentification par session n'est pas activée
- Vous utilisez uniquement JWT (sans sessions)

Pour vérifier votre connexion :
- Essayez d'accéder à http://127.0.0.1:8000/api/users/profile/
- Si vous êtes connecté, vous verrez vos informations
- Sinon, vous aurez une erreur 401

### 5. Tester les permissions authentifié

#### ✅ Lecture autorisée :
- http://127.0.0.1:8000/api/projects/
- http://127.0.0.1:8000/api/projects/1/
- http://127.0.0.1:8000/api/projects/1/issues/

#### ❌ Modification non autorisée (si pas auteur) :
1. Allez sur un projet dont vous n'êtes pas l'auteur
2. Essayez de le modifier via le formulaire
3. Vous obtiendrez : `"detail": "You do not have permission to perform this action."`

## 🔧 Méthode 2 : Extension de navigateur (ModHeader)

### 1. Installer l'extension
- **Chrome** : ModHeader
- **Firefox** : Modify Header Value

### 2. Obtenir un token JWT
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}'
```

Réponse :
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### 3. Configurer l'extension
- Name: `Authorization`
- Value: `Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...` (votre token)

### 4. Naviguer avec authentification
Maintenant, vous pouvez accéder aux endpoints protégés.

## 📊 Scénarios de test des permissions

### Test 1 : Création de projet
1. **Connecté** : POST sur http://127.0.0.1:8000/api/projects/
   - ✅ Formulaire de création disponible
   - ✅ Projet créé avec vous comme auteur

### Test 2 : Modification d'un projet
1. **Votre projet** : PUT sur http://127.0.0.1:8000/api/projects/1/
   - ✅ Formulaire de modification disponible
   
2. **Projet d'un autre** : PUT sur http://127.0.0.1:8000/api/projects/2/
   - ❌ Erreur 403 Forbidden

### Test 3 : Ajout de contributeur
1. **Votre projet** : POST sur http://127.0.0.1:8000/api/projects/1/add_contributor/
   ```json
   {"user_id": 2}
   ```
   - ✅ Contributeur ajouté

2. **Projet d'un autre** : 
   - ❌ Erreur 403 Forbidden

## 🎨 Console du navigateur (DevTools)

### Tests avec JavaScript
Ouvrez la console (F12) et testez :

```javascript
// Test sans authentification
fetch('http://127.0.0.1:8000/api/projects/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Erreur:', error));

// Test avec token
const token = 'votre_token_ici';
fetch('http://127.0.0.1:8000/api/projects/', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data));

// Test de création
fetch('http://127.0.0.1:8000/api/projects/', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        name: 'Test Browser',
        description: 'Projet créé depuis le navigateur',
        type: 'back-end'
    })
})
.then(response => response.json())
.then(data => console.log('Projet créé:', data));
```

## 📋 Résumé des permissions

| Action | Non authentifié | Authentifié | Auteur | Admin |
|--------|----------------|-------------|---------|--------|
| Inscription | ✅ | ✅ | ✅ | ✅ |
| Voir projets | ❌ | ✅ | ✅ | ✅ |
| Créer projet | ❌ | ✅ | ✅ | ✅ |
| Modifier projet | ❌ | ❌ | ✅ | ✅ |
| Supprimer projet | ❌ | ❌ | ✅ | ✅ |
| Ajouter contributeur | ❌ | ❌ | ✅ | ✅ |

## 💡 Astuces

1. **Session persistante** : L'authentification via l'interface DRF utilise les sessions, donc vous restez connecté entre les pages.

2. **Format JSON** : Ajoutez `?format=json` à l'URL pour forcer le format JSON :
   - http://127.0.0.1:8000/api/projects/?format=json

3. **Debug** : Les erreurs de permission sont très explicites dans l'interface DRF.

4. **Logout** : Cliquez sur votre username puis "Log out" pour tester à nouveau sans authentification.

---

**Note** : L'interface web de Django REST Framework est l'outil le plus pratique pour tester rapidement les permissions sans outils externes.
