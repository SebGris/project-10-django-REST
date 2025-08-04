# 🔐 Résumé des Permissions SoftDesk

## Règle Fondamentale
**⚠️ Seuls les contributeurs d'un projet peuvent accéder à ce dernier et à toutes ses ressources (issues, comments).**

## Classes de Permissions

### 1. `IsProjectAuthorOrContributor`
- **Utilisée pour** : Projects
- **Règles** :
  - ✅ Contributeurs peuvent lire
  - ✅ Auteur peut tout faire (CRUD + gérer contributeurs)
  - ❌ Non-contributeurs n'ont aucun accès

### 2. `IsProjectContributor`
- **Utilisée pour** : Vérification de base pour Issues/Comments
- **Règles** :
  - ✅ Contributeurs ont accès
  - ❌ Non-contributeurs sont bloqués

### 3. `IsAuthorOrProjectAuthorOrReadOnly`
- **Utilisée pour** : Issues et Comments
- **Règles** :
  - ✅ Contributeurs peuvent lire
  - ✅ Auteur de l'objet peut modifier/supprimer
  - ✅ Auteur du projet peut tout faire
  - ❌ Non-contributeurs n'ont aucun accès

### 4. `IsOwnerOrReadOnly`
- **Utilisée pour** : Profils utilisateur
- **Règles** :
  - ✅ Propriétaire peut modifier son profil
  - ✅ Autres peuvent lire (données limitées RGPD)

## Implémentation dans les ViewSets

```python
# Projects
permission_classes = [IsAuthenticated, IsProjectAuthorOrContributor]

# Issues
permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrProjectAuthorOrReadOnly]

# Comments
permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrProjectAuthorOrReadOnly]

# Users
permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
```

## Tests de Vérification
Utilisez la collection Postman `softdesk-permissions-complete-tests.json` pour vérifier que toutes ces règles sont respectées.
