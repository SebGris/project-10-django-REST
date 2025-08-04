# 🔄 Utiliser plusieurs collections Postman ensemble

## ✅ OUI, vous pouvez utiliser les deux collections !

Les collections "SoftDesk API - Tests Complets" et "SoftDesk - Tests Permissions Projets" peuvent coexister dans le même workspace Postman.

## 🎯 Points importants

### 1. Variables partagées
Les deux collections utilisent les mêmes variables d'environnement :
- `access_token` : Token JWT actuel
- `api_url` : URL de base de l'API
- `user_id`, `project_id`, etc.

### 2. Gestion des tokens
Quand vous changez de collection, le token reste actif car il est stocké dans l'environnement.

### 3. Workflow recommandé

#### Option A : Tester les permissions spécifiquement
1. Utiliser "SoftDesk - Tests Permissions Projets"
2. Commencer par "1️⃣ Setup - Création des utilisateurs"
3. Suivre l'ordre des dossiers

#### Option B : Tests généraux de l'API
1. Utiliser "SoftDesk API - Tests Complets"
2. Se connecter avec un utilisateur existant
3. Tester les fonctionnalités

## 🔧 Résolution du problème d'authentification

### Le problème
L'héritage de l'authentification depuis la collection ne fonctionne pas toujours correctement dans Postman.

### Solutions

#### Solution 1 : Forcer le Bearer Token (Recommandé)
Pour chaque requête qui nécessite une authentification :
1. Onglet "Authorization"
2. Type : "Bearer Token"
3. Token : `{{access_token}}`

#### Solution 2 : Vérifier l'héritage
1. Onglet "Authorization"
2. Type : "Inherit auth from parent"
3. Vérifier que la collection a bien Bearer Token configuré

#### Solution 3 : Script Pre-request global
Ajouter dans les Pre-request Scripts de la collection :
```javascript
if (pm.request.headers.has('Authorization')) {
    pm.request.headers.upsert({
        key: 'Authorization',
        value: 'Bearer ' + pm.environment.get('access_token')
    });
}
```

## 📝 Bonnes pratiques

1. **Un environnement unique** : Utilisez "SoftDesk Local" pour les deux collections
2. **Tokens à jour** : Relancez le login si vous avez des erreurs 401
3. **Console Postman** : View > Show Postman Console pour débugger
4. **Variables** : Vérifiez les variables dans Environment > SoftDesk Local

## 🚀 Exemple de workflow mixte

1. **Collection principale** : Créer un utilisateur admin
2. **Collection permissions** : Tester les scénarios Alice/Bob/Charlie
3. **Collection principale** : Nettoyer les données de test

Les deux collections sont complémentaires et peuvent être utilisées ensemble sans problème !
