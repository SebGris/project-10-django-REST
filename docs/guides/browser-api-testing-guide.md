# 📮 Guide : Tester les permissions de l'API avec Postman

## 🚀 Configuration initiale avec Postman

Postman est l'outil recommandé pour tester efficacement les permissions et accès de l'API SoftDesk.

### 1. Prérequis
- Serveur Django démarré : `poetry run python manage.py runserver`
- Collection Postman importée (voir [Guide Postman](../postman/postman-guide.md))
- Environnement "SoftDesk Local" sélectionné

### 2. Workflow de test recommandé

1. **Obtenir un token JWT** : Exécuter `🔐 Authentication > Obtenir Token JWT`
2. **Vérifier l'authentification** : Tester `👥 Users > Profil Personnel (GET)`
3. **Créer des ressources** : Projet → Issue → Comment
4. **Tester les permissions** : Modifier/supprimer avec différents utilisateurs

## 📊 Scénarios de test des permissions

### Test 1 : Accès sans authentification

1. **Désactiver temporairement le token** :
   - Dans l'onglet "Authorization" de la requête
   - Sélectionner "No Auth" au lieu de "Inherit auth from parent"

2. **Tester les endpoints publics vs protégés** :
   ```
   ✅ POST /api/users/          → 201 Created (inscription publique)
   ❌ GET  /api/projects/        → 401 Unauthorized
   ❌ GET  /api/users/profile/   → 401 Unauthorized
   ```

### Test 2 : Permissions selon le rôle

#### Étape 1 : Se connecter en tant qu'admin
```json
POST /api/token/
{
    "username": "admin",
    "password": "SoftDesk2025!"
}
```

#### Étape 2 : Créer un projet
```json
POST /api/projects/
{
    "name": "Projet Admin",
    "description": "Projet créé par admin",
    "type": "back-end"
}
// Notez l'ID du projet créé
```

#### Étape 3 : Changer d'utilisateur
```json
POST /api/token/
{
    "username": "john_doe_1754220224",
    "password": "SecurePass123!"
}
```

#### Étape 4 : Tester les permissions
```
❌ PUT    /api/projects/{id}/  → 403 Forbidden (pas l'auteur)
❌ DELETE /api/projects/{id}/  → 403 Forbidden (pas l'auteur)
✅ GET    /api/projects/{id}/  → 200 OK (lecture autorisée)
```

### Test 3 : Contributeurs

1. **En tant qu'auteur du projet** : Ajouter un contributeur
   ```json
   POST /api/projects/{id}/add_contributor/
   {
       "user_id": 2
   }
   ```

2. **En tant que contributeur** : Créer une issue
   ```json
   POST /api/projects/{id}/issues/
   {
       "name": "Issue du contributeur",
       "description": "Test des permissions contributeur",
       "tag": "BUG",
       "priority": "MEDIUM",
       "status": "To Do"
   }
   ```

## 🔢 Codes de réponse et leur signification

### Vue d'ensemble dans Postman

| Code | Couleur | Signification | Action corrective |
|------|---------|---------------|-------------------|
| **200** | 🟢 Vert | Lecture réussie | - |
| **201** | 🟢 Vert | Création réussie | - |
| **204** | 🟢 Vert | Suppression réussie | - |
| **400** | 🟠 Orange | Données invalides | Vérifier le body |
| **401** | 🔴 Rouge | Non authentifié | Obtenir un token |
| **403** | 🔴 Rouge | Pas autorisé | Changer d'utilisateur |
| **404** | 🔴 Rouge | Ressource introuvable | Vérifier l'ID |

### Exemples concrets dans Postman

#### ✅ Succès (200/201)
- **Body** : Contient les données de la ressource
- **Headers** : Token valide accepté
- **Tests** : Tous en vert

#### ❌ Erreur d'authentification (401)
```json
{
    "detail": "Authentication credentials were not provided."
}
// Solution : Exécuter "Obtenir Token JWT"
```

#### ❌ Erreur de permission (403)
```json
{
    "detail": "You do not have permission to perform this action."
}
// Solution : Vérifier que vous êtes l'auteur de la ressource
```

#### ❌ Erreur de validation (400)
```json
{
    "age": ["L'âge minimum requis est de 15 ans (conformité RGPD)."],
    "type": ["Type invalide. Choisir parmi: ['back-end', 'front-end', 'iOS', 'Android']"]
}
// Solution : Corriger les données dans le body
```

## 🎯 Tests automatisés avec Postman

### Comment exécuter plusieurs tests d'un coup

Postman permet d'exécuter automatiquement une série de requêtes pour tester rapidement les permissions.

#### Option 1 : Exécuter manuellement chaque requête

1. **Cliquer sur chaque requête** dans l'ordre :
   - `🔐 Authentication > Obtenir Token JWT` (en premier !)
   - `📋 Projects > Créer Projet`
   - `🔒 Tests de Permissions > Accès sans token (401)`
   - etc.

2. **Vérifier le code de réponse** pour chaque requête

#### Option 2 : Utiliser le Runner (automatique)

1. **Ouvrir le Runner** : Cliquer sur "Runner" en bas à gauche de Postman

2. **Faire glisser ce que vous voulez tester** :
   
   - **Pour tester TOUT** : Glissez "SoftDesk API - Tests Complets" (la collection entière)
     ```
     Cela exécutera TOUTES les requêtes dans l'ordre :
     - Authentication
     - Users
     - Projects
     - Issues
     - Comments
     - Tests de Permissions
     ```
   
   - **Pour tester SEULEMENT les permissions** : Glissez "🔒 Tests de Permissions" (le dossier)
     ```
     Cela exécutera seulement :
     - Accès sans token (401)
     - Token invalide (401)
     ```

3. **Configurer le Runner** :
   - **Environment** : Sélectionner "SoftDesk Local"
   - **Iterations** : 1 (nombre de fois à exécuter)
   - **Delay** : 0 (pas de délai entre les requêtes)

4. **Cliquer sur "Run"**

### ⚠️ Important : Ordre d'exécution

Si vous exécutez **toute la collection**, assurez-vous que :
1. **"Obtenir Token JWT"** est exécuté EN PREMIER
2. Les requêtes sont dans le bon ordre (création avant modification)

Si vous exécutez **seulement un dossier** :
- Le dossier "🔒 Tests de Permissions" peut être exécuté seul
- Les autres dossiers nécessitent d'avoir un token valide

### Exemple concret : Tester uniquement les permissions

1. **D'abord, obtenir un token** :
   - Exécuter manuellement : `🔐 Authentication > Obtenir Token JWT`

2. **Ensuite, lancer le Runner** :
   - Glisser le dossier "🔒 Tests de Permissions"
   - Cliquer "Run"

3. **Résultats attendus** :
   ```
   ❌ Accès sans token (401)     → 401 Unauthorized ✅ (c'est normal !)
   ❌ Token invalide (401)       → 401 Unauthorized ✅ (c'est normal !)
   ```

## 📝 Scripts de test automatiques

Chaque requête contient des tests automatiques :

```javascript
// Exemple de test automatique
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has access token", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access');
    pm.environment.set("access_token", jsonData.access);
});
```

## 🔧 Dépannage

### Token expiré
- Exécuter la requête **Refresh Token**
- Ou refaire un **Login**

### Erreur 404
- Vérifier que le serveur Django est lancé
- Vérifier l'URL de base dans les variables

### Erreur 401
- Vérifier que le token est bien défini
- Refaire l'authentification

## 📚 Export des résultats

1. Après les tests, cliquer sur **Export Results**
2. Choisir le format (JSON, HTML, JUnit)
3. Partager avec l'équipe

---

*La collection Postman est mise à jour avec chaque nouvelle version de l'API.*
{{$guid}}           // GUID unique
```

## 🧪 **Tests Automatiques Intégrés**

### **Exemples de tests dans la collection :**

```javascript
// Test de création réussie
pm.test('Utilisateur créé avec succès', () => {
    pm.expect(response.username).to.exist;
});

// Test de conformité RGPD
pm.test('Inscription refusée pour moins de 15 ans', () => {
    pm.expect(pm.response.code).to.equal(400);
});

// Test d'authentification
pm.test('Token obtenu avec succès', () => {
    pm.expect(response.access).to.exist;
});
```

## 📊 **Exécution en Lot (Collection Runner)**

### **Pour tester toute la collection d'un coup :**

1. **Collection SoftDesk API** → **...** → **Run collection**
2. **Sélectionner l'environnement** : `SoftDesk Local`
3. **Order** : Garder l'ordre (important pour les dépendances)
4. **Cliquer "Run SoftDesk API"**

### **Résultat attendu :**
```
✅ 🔐 Authentication → Obtenir Token JWT
✅ 👥 Users → Inscription (Public)
❌ 👥 Users → Test RGPD - <15 ans (échec attendu)
✅ 👥 Users → Profil Personnel
✅ 📋 Projects → Créer Projet
✅ 📋 Projects → Liste des Projets
❌ 🔒 Tests → Accès sans token (échec attendu)
```

## 🔧 **Personnalisation Avancée**

### **Modifier les identifiants de test :**

Dans `Obtenir Token JWT`, modifier le body :
```json
{
    "username": "votre_admin",
    "password": "votre_mot_de_passe"
}
```

### **Tester avec différents types de projets :**

Dans `Créer Projet`, modifier le type :
```json
{
    "type": "front-end"    // Ou "iOS", "Android"
}
```

### **Ajouter de nouveaux tests :**

```javascript
// Dans l'onglet "Tests" d'une requête
pm.test("Mon nouveau test", () => {
    pm.expect(pm.response.code).to.equal(200);
});
```

## 🌐 **Compatibilité Versions**

### **Postman 11.54.6** ✅
- **Format Collection** : v2.1.0 (compatible)
- **Variables d'environnement** : Supportées
- **Scripts pré/post-requête** : Supportés
- **Tests automatiques** : Supportés

### **Versions antérieures**
- **Postman 10.x** ✅ Compatible
- **Postman 9.x** ✅ Compatible (avec limitations mineures)

## 🚨 **Dépannage**

### **Problème : "Could not get response"**
```bash
# Vérifier que le serveur Django est démarré
poetry run python manage.py runserver
```

### **Problème : "401 Unauthorized"**
1. **Exécuter** "Obtenir Token JWT" en premier
2. **Vérifier** que l'environnement "SoftDesk Local" est sélectionné
3. **Vérifier** les identifiants admin

### **Problème : Variables non mises à jour**
1. **Environnement** → **Sélectionner "SoftDesk Local"**
2. **Variables** → **Vérifier les valeurs**
3. **Re-exécuter** "Obtenir Token JWT"

### **Problème : Tests RGPD échouent**
C'est **normal** ! Les tests suivants **doivent échouer** :
- ❌ "Test RGPD - <15 ans" → Code 400 attendu
- ❌ "Accès sans token" → Code 401 attendu

## 🔄 Changer d'utilisateur dans Postman

### Méthode 1 : Modifier la requête d'authentification

1. **Dans la collection Postman, allez à** : `🔐 Authentication` > `Obtenir Token JWT`

2. **Modifiez le body avec les identifiants d'un autre utilisateur** :
   ```json
   {
       "username": "john_doe_1754220224",
       "password": "SecurePass123!"
   }
   ```

3. **Envoyez la requête** : Le nouveau token sera automatiquement sauvegardé dans `{{access_token}}`

4. **Toutes vos prochaines requêtes** utiliseront ce nouveau token (donc le nouvel utilisateur)

### Méthode 2 : Créer plusieurs environnements

1. **Créez un environnement par utilisateur** :
   - Environment 1 : `Admin`
   - Environment 2 : `John Doe`
   - Environment 3 : `Test User`

2. **Dans chaque environnement, stockez** :
   ```
   username: john_doe_1754220224
   password: SecurePass123!
   access_token: (sera rempli après authentification)
   ```

3. **Changez d'environnement** pour changer d'utilisateur

### Exemple pratique : Tester les permissions

```javascript
// 1. Connectez-vous en tant qu'admin
POST /api/token/
{
    "username": "admin",
    "password": "SoftDesk2025!"
}

// 2. Créez un projet (vous serez l'auteur)
POST /api/projects/
{
    "name": "Projet Admin",
    "description": "Créé par admin",
    "type": "back-end"
}
// Réponse : {"id": 1, "author": {...}, ...}

// 3. Connectez-vous en tant qu'autre utilisateur
POST /api/token/
{
    "username": "john_doe_1754220224",
    "password": "SecurePass123!"
}

// 4. Essayez de modifier le projet de l'admin
PUT /api/projects/1/
{
    "name": "Projet modifié par John",
    "description": "Tentative de modification",
    "type": "front-end"
}
// Réponse : 403 Forbidden - "You do not have permission to perform this action."

// 5. Créez votre propre projet
POST /api/projects/
{
    "name": "Projet John",
    "description": "Créé par John",
    "type": "iOS"
}
// Réponse : 201 Created - Succès car John crée son propre projet
```

### 📝 Liste des utilisateurs pour tests

Pour voir tous les utilisateurs disponibles :
1. **Connectez-vous en tant qu'admin**
2. **Envoyez** : `GET /api/users/`
3. **Notez les usernames** pour vous connecter avec eux

### ⚡ Script de test automatique

Dans l'onglet "Pre-request Script" de votre collection :

```javascript
// Rotation automatique d'utilisateurs pour les tests
const users = [
    { username: "admin", password: "SoftDesk2025!" },
    { username: "john_doe_1754220224", password: "SecurePass123!" },
    { username: "SEB", password: "VotreMotDePasse!" }
];

// Sélectionner un utilisateur aléatoire
const randomUser = users[Math.floor(Math.random() * users.length)];
pm.environment.set("current_username", randomUser.username);
pm.environment.set("current_password", randomUser.password);
```

Puis dans le body de votre requête d'authentification :
```json
{
    "username": "{{current_username}}",
    "password": "{{current_password}}"
}
```

### 🔑 Points importants

- **Le token JWT contient l'identité** : Changer de token = changer d'utilisateur
- **Les permissions sont vérifiées côté serveur** : Le token détermine qui vous êtes
- **Gardez les mots de passe en sécurité** : Utilisez les variables d'environnement Postman

---

**🚀 Votre collection Postman est prête pour une démonstration parfaite de l'API SoftDesk !**