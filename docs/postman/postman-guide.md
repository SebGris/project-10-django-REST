# 📮 Guide Postman - Collection SoftDesk API

[← Retour à la documentation](../README.md) | [API Guide](../api/api-guide.md) | [Tests API](../api/api-testing-complete-guide.md)

## 📋 Navigation
- [Installation](#installation)
- [Import de la collection](#import-de-la-collection)
- [Configuration](#configuration)
- [Tests disponibles](#tests-disponibles)
- [Variables d'environnement](#variables-denvironnement)

## 🚀 Installation

1. **Télécharger Postman** : [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
2. **Créer un compte** (optionnel mais recommandé)

## 📥 Import de la collection

1. Ouvrir Postman
2. Cliquer sur **Import** (bouton en haut à gauche)
3. Sélectionner le fichier : `docs/postman/softdesk-api-collection.json`
4. La collection **SoftDesk API** apparaît dans le panneau gauche

### Import de l'environnement

1. Cliquer à nouveau sur **Import**
2. Sélectionner le fichier : `docs/postman/softdesk-environment.json`
3. L'environnement **SoftDesk Local** est maintenant disponible

## ⚙️ Configuration

### Variables d'environnement

Sélectionner l'environnement **SoftDesk Local** dans le menu déroulant en haut à droite de l'interface Postman.

Les variables suivantes sont déjà configurées dans l'environnement importé :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `base_url` | `http://127.0.0.1:8000` | URL de base de l'API |
| `username` | `admin` | Nom d'utilisateur |
| `password` | `SoftDesk2025!` | Mot de passe |
| `access_token` | *(généré automatiquement)* | Token JWT |
| `refresh_token` | *(généré automatiquement)* | Refresh token |

## 🧪 Tests disponibles

### 1. Authentification
- **Login** : Obtenir les tokens JWT
- **Refresh Token** : Renouveler l'access token

### 2. Utilisateurs
- **Créer un utilisateur** : Inscription
- **Liste des utilisateurs** : Voir tous les utilisateurs
- **Profil utilisateur** : Voir/modifier son profil

### 3. Projets
- **Liste des projets** : Projets où je suis contributeur
- **Créer un projet** : Nouveau projet
- **Détails projet** : Voir un projet spécifique
- **Modifier projet** : Mettre à jour (auteur uniquement)
- **Supprimer projet** : Effacer (auteur uniquement)

### 4. Contributeurs
- **Liste contributeurs** : Voir les contributeurs d'un projet
- **Ajouter contributeur** : Inviter un utilisateur
- **Retirer contributeur** : Enlever un utilisateur

### 5. Issues
- **Liste issues** : Issues d'un projet
- **Créer issue** : Nouvelle issue
- **Détails issue** : Voir une issue
- **Modifier issue** : Mettre à jour
- **Supprimer issue** : Effacer

### 6. Commentaires
- **Liste commentaires** : Commentaires d'une issue
- **Créer commentaire** : Nouveau commentaire
- **Modifier commentaire** : Éditer
- **Supprimer commentaire** : Effacer

## 🔄 Workflow de test

1. **Authentification**
   - Exécuter "Login" pour obtenir les tokens
   - Les tokens sont automatiquement sauvegardés

2. **Créer des données**
   - Créer un utilisateur
   - Créer un projet
   - Ajouter des contributeurs
   - Créer des issues
   - Ajouter des commentaires

3. **Tester les permissions**
   - Essayer de modifier un projet dont vous n'êtes pas l'auteur
   - Tenter d'accéder à un projet où vous n'êtes pas contributeur

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

## 🎯 Collection Runner

Pour exécuter tous les tests :

1. Cliquer sur **Runner** (en bas de Postman)
2. Sélectionner la collection **SoftDesk API**
3. Choisir l'environnement **SoftDesk Local**
4. Cliquer sur **Run SoftDesk API**

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
