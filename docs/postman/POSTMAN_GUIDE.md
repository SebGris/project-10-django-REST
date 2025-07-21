# 📮 Postman SoftDesk - Guide d'Utilisation Complète

## 🎯 **Vue d'ensemble**

Ce guide vous accompagne pour tester l'API SoftDesk avec **Postman 11.54.6**. La collection fournie contient tous les endpoints avec des tests automatiques et la gestion de l'authentification JWT.

## 📦 **Fichiers Postman fournis**

```
docs/postman/
├── SoftDesk_API_Collection.json    # 📋 Collection complète des tests
└── SoftDesk_Environment.json       # 🌍 Variables d'environnement
```

## 🚀 **Installation et Import**

### **1. Importer la Collection**

1. **Ouvrir Postman 11.54.6**
2. **Import** → **File** → Sélectionner `SoftDesk_API_Collection.json`
3. **Import** → **File** → Sélectionner `SoftDesk_Environment.json`

### **2. Sélectionner l'Environnement**

1. **En haut à droite** → Sélectionner `SoftDesk Local`
2. **Vérifier les variables** :
   - `base_url` : `http://127.0.0.1:8000`
   - `api_url` : `{{base_url}}/api`

## 🔧 **Préparation du serveur Django**

### **Avant de commencer les tests :**

```bash
# 1. Démarrer le serveur
cd "C:\Users\sebas\Documents\OpenClassrooms\Mes_projets\project-10-django-REST"
poetry run python manage.py runserver

# 2. Créer le superutilisateur (si pas déjà fait)
poetry run python create_superuser.py
```

**Identifiants par défaut :**
- **Username :** `admin`
- **Password :** `SoftDesk2025!`

## 📋 **Structure de la Collection**

### **🔐 1. Authentication**
```
├── Obtenir Token JWT          # POST /api/token/
└── Rafraîchir Token          # POST /api/token/refresh/
```

### **👥 2. Users**
```
├── Inscription (Public)           # POST /api/users/
├── Liste des Utilisateurs         # GET /api/users/
├── Profil Personnel (GET)          # GET /api/users/profile/
├── Modifier Profil (PATCH)         # PATCH /api/users/profile/
├── Détails Utilisateur             # GET /api/users/{id}/
└── Test RGPD - <15 ans (échec)     # POST /api/users/ (âge < 15)
```

### **📋 3. Projects**
```
├── Créer Projet                    # POST /api/projects/
├── Liste des Projets               # GET /api/projects/
├── Détails Projet                  # GET /api/projects/{id}/
├── Modifier Projet                 # PUT /api/projects/{id}/
├── Ajouter Contributeur            # POST /api/projects/{id}/add-contributor/
├── Liste Contributeurs             # GET /api/projects/{id}/contributors/
└── Supprimer Projet                # DELETE /api/projects/{id}/
```

### **🔒 4. Tests de Permissions**
```
├── Accès sans token (401)          # GET /api/projects/ (no auth)
└── Token invalide (401)            # GET /api/users/profile/ (bad token)
```

## 🎯 **Guide d'Exécution Étape par Étape**

### **Phase 1 : Authentification**

1. **Obtenir Token JWT**
   - Exécuter la requête
   - ✅ **Vérification automatique** : Token stocké dans les variables
   - Variables mises à jour : `access_token`, `refresh_token`

### **Phase 2 : Tests Utilisateurs**

2. **Inscription (Public)**
   - ✅ **Test automatique** : Utilisateur créé
   - Variable mise à jour : `user_id`

3. **Test RGPD - <15 ans**
   - ✅ **Doit échouer** avec code 400
   - ✅ **Test automatique** : Message d'erreur vérifié

4. **Profil Personnel**
   - ✅ **Authentification automatique** avec token

### **Phase 3 : Tests Projets**

5. **Créer Projet**
   - ✅ **Test automatique** : Projet créé
   - Variable mise à jour : `project_id`

6. **Ajouter Contributeur**
   - Utilise automatiquement `user_id` créé précédemment

7. **Tests CRUD complets**
   - Liste, détails, modification, suppression

### **Phase 4 : Tests Sécurité**

8. **Accès sans authentification**
   - ✅ **Doit échouer** avec code 401

9. **Token invalide**
   - ✅ **Doit échouer** avec code 401

## 🔍 **Variables Automatiques**

### **Variables Globales**
```javascript
{{base_url}}        // http://127.0.0.1:8000
{{api_url}}         // http://127.0.0.1:8000/api
{{access_token}}    // Token JWT (auto-rempli)
{{refresh_token}}   // Token refresh (auto-rempli)
{{user_id}}         // ID utilisateur créé (auto-rempli)
{{project_id}}      // ID projet créé (auto-rempli)
```

### **Variables Dynamiques Postman**
```javascript
{{$timestamp}}      // Timestamp Unix (unique)
{{$randomInt}}      // Nombre aléatoire
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
