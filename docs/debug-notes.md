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
