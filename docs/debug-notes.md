# Notes de débogage

## Erreur : "Cannot query User: Must be Contributor instance"

### Problème
Lors de la suppression d'un projet, Django levait une `ValueError` car on essayait de filtrer les projets avec un objet `User` directement :
```python
Project.objects.filter(contributors=self.request.user)  # ❌ Incorrect
```

### Cause
Le champ `contributors` est une relation ManyToMany vers le modèle `Contributor`, pas directement vers `User`. La structure est :
- `Project` → ManyToMany → `Contributor`
- `Contributor` → ForeignKey → `User`

### Solution
Utiliser la notation correcte pour traverser les relations :
```python
Project.objects.filter(contributors__user=self.request.user).distinct()  # ✅ Correct
```

Le `.distinct()` est important car la jointure peut créer des doublons si un utilisateur est contributeur plusieurs fois (ce qui ne devrait pas arriver, mais par sécurité).

### Alternative (si on change le modèle)
Une alternative serait de simplifier le modèle en ayant une relation directe :
```python
class Project(models.Model):
    contributors = models.ManyToManyField(User, related_name='projects')
```
Mais cela nécessiterait de refactoriser tout le code existant.

## Erreur : "You do not have permission to perform this action" pour les contributeurs

### Problème
Alice ne pouvait pas accéder à son propre projet malgré le fait qu'elle en soit l'auteur.

### Cause
1. La vérification `obj.contributors.filter(id=request.user.id)` était incorrecte
2. L'auteur n'était pas automatiquement ajouté comme contributeur lors de la création

### Solutions appliquées

#### 1. Correction de la vérification des permissions
```python
# ❌ Incorrect - cherche un ID d'utilisateur dans les contributeurs
obj.contributors.filter(id=request.user.id).exists()

# ✅ Correct - cherche via la relation user
obj.contributors.filter(user=request.user).exists()
```

#### 2. Ajout automatique de l'auteur comme contributeur
```python
def perform_create(self, serializer):
    project = serializer.save(author=self.request.user)
    # Ajouter automatiquement l'auteur comme contributeur
    Contributor.objects.create(user=self.request.user, project=project)
```

### Vérification
Après ces corrections :
- L'auteur est automatiquement contributeur de son projet
- Les permissions vérifient correctement la relation Contributor → User
- Alice peut maintenant accéder à ses projets
