# 🔄 Django get_or_create() et defaults - Guide Complet

[← Retour aux guides Django](./README.md) | [Django Guide](./django-guide.md)

## 📋 Navigation
- [Concept de base](#concept-de-base)
- [Le paramètre defaults](#le-paramètre-defaults)
- [Exemples pratiques](#exemples-pratiques)
- [Cas d'usage dans SoftDesk](#cas-dusage-dans-softdesk)
- [Bonnes pratiques](#bonnes-pratiques)

## 🎯 Concept de base

La méthode `get_or_create()` de Django permet de récupérer un objet ou de le créer s'il n'existe pas. Elle retourne un tuple : `(objet, created)` où `created` est un booléen indiquant si l'objet a été créé.

## Le paramètre defaults

### Sans `defaults` - Tous les paramètres sont utilisés pour la recherche

```python
# Recherche un utilisateur avec TOUS ces critères
user, created = User.objects.get_or_create(
    username="john_doe",
    email="john@example.com",
    age=25
)
```

**Comportement :**
- Django cherche : `username="john_doe"` ET `email="john@example.com"` ET `age=25`
- Si un utilisateur "john_doe" existe avec un email ou âge différent → Création d'un nouveau

### Avec `defaults` - Séparation recherche/création

```python
# Recherche SEULEMENT par username
user, created = User.objects.get_or_create(
    username="john_doe",
    defaults={
        "email": "john@example.com",
        "age": 25
    }
)
```

**Comportement :**
- Django cherche SEULEMENT : `username="john_doe"`
- Si trouvé → retourne l'utilisateur existant (ignore les `defaults`)
- Si non trouvé → crée avec username + les valeurs dans `defaults`

## Exemples pratiques

### Exemple 1 : Gestion des contributeurs de projet

```python
# ✅ Bon usage - On veut un seul contributeur par couple (user, project)
contributor, created = Contributor.objects.get_or_create(
    user=user,
    project=project,
    defaults={
        "role": "CONTRIBUTOR",
        "permissions": "READ_ONLY"
    }
)
```

### Exemple 2 : Configuration utilisateur

```python
# ✅ Bon usage - Une config par utilisateur, valeurs par défaut à la création
config, created = UserConfig.objects.get_or_create(
    user=user,
    defaults={
        "theme": "dark",
        "notifications_enabled": True,
        "language": "fr"
    }
)
```

### Exemple 3 : Sans defaults quand tous les champs sont des critères

```python
# ✅ Pas besoin de defaults si tous les champs sont des critères de recherche
tag, created = Tag.objects.get_or_create(
    name="python",
    category="programming"
)
```

## Cas d'usage dans SoftDesk

### Ajout automatique de l'auteur comme contributeur

```python
# Dans Project.save()
if is_new:
    Contributor.objects.get_or_create(
        user=self.author,
        project=self
    )
```

**Pourquoi pas de `defaults` ici ?**
- Le modèle `Contributor` n'a que 3 champs : `user`, `project`, `created_time`
- `created_time` est automatique (`auto_now_add=True`)
- Pas d'autres champs à définir lors de la création

### Si on avait un champ `role` dans Contributor

```python
# Exemple hypothétique avec un champ role
if is_new:
    Contributor.objects.get_or_create(
        user=self.author,
        project=self,
        defaults={
            "role": "OWNER",
            "can_delete": True
        }
    )
```

## Bonnes pratiques

1. **Utilisez `defaults` pour** :
   - Les champs avec valeurs par défaut
   - Les champs qui ne sont pas des critères d'unicité
   - Les métadonnées (date de création manuelle, etc.)

2. **N'utilisez pas `defaults` pour** :
   - Les champs qui font partie de l'unicité
   - Quand tous les champs sont des critères de recherche

3. **Gérez les retours** :
   ```python
   obj, created = Model.objects.get_or_create(...)
   if created:
       print("Nouvel objet créé")
   else:
       print("Objet existant récupéré")
   ```

## 🔗 Ressources

- [Documentation Django officielle](https://docs.djangoproject.com/en/stable/ref/models/querysets/#get-or-create)
- [Guide Django](./django-guide.md)
- [Retour au sommaire](../../README.md)