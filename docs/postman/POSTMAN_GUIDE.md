# 📮 Guide Postman - Collection SoftDesk API

[← Retour à la documentation](../README.md) | [API Guide](../API_GUIDE.md) | [Tests API](../API_TESTING_COMPLETE_GUIDE.md)

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
3. Sélectionner le fichier : `docs/postman/SoftDesk_API.postman_collection.json`
4. La collection **SoftDesk API** apparaît dans le panneau gauche

## ⚙️ Configuration

### Variables d'environnement

Créer un environnement **SoftDesk Local** :

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

## 📈 **Métriques de Validation**

### **Collection complète = 12+ requêtes**
- ✅ **8-10 succès** (authentification, CRUD)
- ❌ **2-3 échecs** (tests sécurité/RGPD - **attendus**)

### **Temps d'exécution :** ~30 secondes

### **Couverture fonctionnelle :**
- ✅ **Authentification JWT** complète
- ✅ **CRUD Utilisateurs** complet
- ✅ **CRUD Projets** complet
- ✅ **Permissions** validées
- ✅ **Conformité RGPD** testée

## 🎯 **Pour OpenClassrooms**

Cette collection Postman démontre :
1. **✅ API fonctionnelle** (tous les endpoints)
2. **✅ Sécurité** (authentification JWT)
3. **✅ Conformité RGPD** (validation âge)
4. **✅ Tests automatisés** (qualité du code)
5. **✅ Documentation pratique** (prêt pour démo)

---

**🚀 Votre collection Postman est prête pour une démonstration parfaite de l'API SoftDesk !**
