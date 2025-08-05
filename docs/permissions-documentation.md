# 🔒 Documentation des Permissions - API SoftDesk

## Règle Fondamentale

**⚠️ IMPORTANT : Seuls les contributeurs d'un projet peuvent accéder à ce dernier et à toutes ses ressources (issues, comments).**

## Matrice des Permissions

### 1. Projects

| Action | Qui peut le faire | Condition |
|--------|-------------------|-----------|
| **Créer** un projet | Tout utilisateur authentifié | - |
| **Lister** les projets | Utilisateur authentifié | Voit uniquement les projets où il est contributeur |
| **Voir** un projet | Contributeurs uniquement | Doit être dans la liste des contributeurs |
| **Modifier** un projet | Auteur uniquement | Doit être l'auteur du projet |
| **Supprimer** un projet | Auteur uniquement | Doit être l'auteur du projet |
| **Ajouter** un contributeur | Auteur uniquement | Doit être l'auteur du projet |
| **Retirer** un contributeur | Auteur uniquement | Doit être l'auteur du projet |

### 2. Issues

| Action | Qui peut le faire | Condition |
|--------|-------------------|-----------|
| **Créer** une issue | Contributeurs du projet | Doit être contributeur du projet |
| **Lister** les issues | Contributeurs du projet | Doit être contributeur du projet |
| **Voir** une issue | Contributeurs du projet | Doit être contributeur du projet |
| **Modifier** une issue | Auteur de l'issue OU Auteur du projet | - |
| **Supprimer** une issue | Auteur de l'issue OU Auteur du projet | - |

### 3. Comments

| Action | Qui peut le faire | Condition |
|--------|-------------------|-----------|
| **Créer** un commentaire | Contributeurs du projet | Doit être contributeur du projet |
| **Lister** les commentaires | Contributeurs du projet | Doit être contributeur du projet |
| **Voir** un commentaire | Contributeurs du projet | Doit être contributeur du projet |
| **Modifier** un commentaire | Auteur du commentaire uniquement | - |
| **Supprimer** un commentaire | Auteur du commentaire OU Auteur du projet | - |

### 4. Users

| Action | Qui peut le faire | Condition |
|--------|-------------------|-----------|
| **S'inscrire** | Tout le monde | Âge >= 15 ans |
| **Lister** les utilisateurs | Utilisateur authentifié | Pour ajouter des contributeurs |
| **Voir** un profil | Utilisateur authentifié | Données limitées selon RGPD |
| **Modifier** un profil | Le propriétaire uniquement | Seulement son propre profil |
| **Supprimer** un compte | Le propriétaire uniquement | Seulement son propre compte |

## Implémentation Technique

### Permissions Personnalisées

```python
class IsProjectContributor(permissions.BasePermission):
    """Vérifie que l'utilisateur est contributeur du projet"""
    
class IsAuthorOrProjectAuthorOrReadOnly(permissions.BasePermission):
    """Permissions pour issues et commentaires : auteur ou auteur du projet"""
    
class IsProjectAuthorOrContributor(permissions.BasePermission):
    """Combine les permissions auteur/contributeur pour les projets"""
```

### ViewSets avec Permissions

```python
class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributor]
    
    def get_queryset(self):
        # Retourne uniquement les projets où l'utilisateur est contributeur
        return Project.objects.filter(contributors=self.request.user)

class IssueViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsProjectContributor]
    
    def get_queryset(self):
        # Filtre automatique basé sur le projet parent
        project = self.get_project()
        if not project.contributors.filter(id=self.request.user.id).exists():
            raise PermissionDenied()
        return Issue.objects.filter(project=project)
```

## Flux de Vérification

1. **Authentification** : L'utilisateur doit avoir un token JWT valide
2. **Contributeur** : Pour accéder à un projet/issue/comment, vérifier que l'utilisateur est dans `project.contributors`
3. **Autorisation** : Selon l'action, vérifier les permissions spécifiques (auteur, etc.)

## Cas d'Usage

### ✅ Autorisé
- Alice crée un projet → Elle devient automatiquement contributrice
- Alice ajoute Bob comme contributeur → Bob peut maintenant voir le projet
- Bob crée une issue dans le projet → Il est contributeur
- Bob commente l'issue → Il est contributeur

### ❌ Refusé (403 Forbidden)
- Charlie essaie de voir le projet d'Alice → Il n'est pas contributeur
- Charlie essaie de créer une issue → Il n'est pas contributeur
- Bob essaie de modifier le projet d'Alice → Il n'est pas l'auteur
- Charlie essaie de voir les issues du projet → Il n'est pas contributeur

## Tests de Permissions

Utilisez la collection Postman `softdesk-permissions-complete-tests.json` pour tester tous ces scénarios.
