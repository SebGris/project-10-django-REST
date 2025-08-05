# 🔍 Vérification des Permissions dans les ViewSets

## Problèmes identifiés et corrections

### 1. **ProjectViewSet** ✅
- **Permissions**: `[IsAuthenticated, IsProjectAuthorOrContributor]`
- **Correction**: Ajout de `get_queryset()` pour filtrer uniquement les projets où l'utilisateur est contributeur
- **Résultat**: Les utilisateurs ne voient que leurs projets

### 2. **ContributorViewSet** ⚠️
- **Problème**: Manquait la permission `IsProjectContributor`
- **Correction**: Ajout de `IsProjectContributor` et vérification dans `get_queryset()`
- **Résultat**: Seuls les contributeurs peuvent voir la liste des contributeurs

### 3. **IssueViewSet** ⚠️
- **Problème**: Utilisait seulement `IsProjectAuthorOrContributor`
- **Correction**: Ajout de `IsProjectContributor` pour vérifier l'accès au projet
- **Résultat**: Seuls les contributeurs peuvent accéder aux issues

### 4. **CommentViewSet** ⚠️
- **Problème**: Utilisait seulement `IsProjectAuthorOrContributor`
- **Correction**: Ajout de `IsProjectContributor` et amélioration du queryset
- **Résultat**: Seuls les contributeurs peuvent accéder aux commentaires

## Configuration correcte des permissions

```python
# Projects
permission_classes = [IsAuthenticated, IsProjectAuthorOrContributor]

# Contributors (lecture seule)
permission_classes = [IsAuthenticated, IsProjectContributor]

# Issues
permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrProjectAuthorOrReadOnly]

# Comments
permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrProjectAuthorOrReadOnly]
```

## Flux de vérification

1. **IsAuthenticated** : L'utilisateur doit être connecté
2. **IsProjectContributor** : L'utilisateur doit être contributeur du projet (pour Issues/Comments)
3. **IsAuthorOrProjectAuthorOrReadOnly** : Pour modifier, doit être auteur de l'objet ou du projet

## Tests recommandés

1. ✅ Un contributeur peut voir le projet et ses ressources
2. ❌ Un non-contributeur ne peut pas voir le projet (403)
3. ❌ Un non-contributeur ne peut pas voir les issues (403)
4. ❌ Un non-contributeur ne peut pas voir les commentaires (403)
5. ✅ L'auteur du projet peut tout modifier
6. ✅ Un contributeur peut créer des issues/commentaires
7. ❌ Un contributeur ne peut pas modifier le projet
