# Implémentation de la création de projet

## Fonctionnalité
> Un utilisateur peut créer un projet. Il en devient l'auteur et le contributeur.

## Comment c'est implémenté dans le code

Cette fonctionnalité est implémentée à travers plusieurs composants du code :

### 1. Dans le modèle `Project`

Le modèle `Project` surcharge la méthode `save()` pour ajouter automatiquement l'auteur comme contributeur lors de la création :

```python
def save(self, *args, **kwargs):
    """
    Surcharge de save pour créer automatiquement l'auteur comme contributeur
    """
    is_new = self.pk is None  # True si c'est une création, False si c'est une mise à jour
    super().save(*args, **kwargs)
    
    # Si c'est un nouveau projet, ajouter l'auteur comme contributeur
    if is_new:
        Contributor.objects.get_or_create(
            user=self.author,
            project=self
        )
```

### 2. Dans `ProjectViewSet`

Le ViewSet définit l'utilisateur courant comme auteur lors de la création :

```python
def perform_create(self, serializer):
    """L'utilisateur devient auteur du projet"""
    serializer.save(author=self.request.user)
```

### 3. Vérification des droits

Le modèle `Project` possède plusieurs méthodes pour vérifier si un utilisateur est contributeur ou auteur :

```python
def is_author_or_contributor(self, user):
    """
    Vérifie si un utilisateur est auteur ou contributeur du projet
    """
    return (self.author == user or 
            self.contributors.filter(user=user).exists())

def can_user_access(self, user):
    """
    Vérifie si un utilisateur peut accéder au projet (auteur ou contributeur)
    """
    return self.is_author_or_contributor(user)

def can_user_modify(self, user):
    """
    Vérifie si un utilisateur peut modifier le projet (seul l'auteur)
    """
    return self.author == user

def is_user_contributor(self, user):
    """
    Vérifie si un utilisateur est contributeur de ce projet
    """
    return self.contributors.filter(user=user).exists() or user == self.author
```

### 4. Permissions personnalisées

Des classes de permission appropriées (`IsProjectAuthor`, `IsAuthorOrProjectAuthor`) sont utilisées pour contrôler l'accès aux vues et assurer que seuls les utilisateurs autorisés peuvent interagir avec les projets.

## Résumé du flux de création

1. Un utilisateur authentifié envoie une requête POST avec les détails du projet
2. `ProjectViewSet.perform_create()` associe l'utilisateur comme auteur
3. `Project.save()` crée automatiquement un enregistrement `Contributor` pour l'auteur
4. L'utilisateur a maintenant un double rôle : auteur (propriétaire) et contributeur

Cela garantit que tout utilisateur qui crée un projet a automatiquement tous les droits nécessaires pour le gérer et y contribuer.
