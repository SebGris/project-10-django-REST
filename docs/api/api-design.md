# Choix de conception de l'API SoftDesk

## Philosophie : Code minimaliste et efficace

### Endpoint `/users/profile/`

L'action `profile` dans `UserViewSet` est un exemple parfait de code minimaliste :

```python
@action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
def profile(self, request):
    """Consulter ou modifier son propre profil"""
    if request.method == 'GET':
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    serializer = self.get_serializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
```

**Pourquoi ce code est optimal :**

1. **Essentiel** : Sans cette action, l'endpoint `/users/profile/` n'existe pas (erreur 404)

2. **Minimal** : Seulement 10 lignes pour gérer GET et PATCH
   - GET : consulter son profil
   - PATCH : modifier son profil (mise à jour partielle)
   - Pas de PUT (inutile car PATCH suffit)

3. **DRY (Don't Repeat Yourself)** :
   - Utilise `get_serializer()` qui applique automatiquement le bon serializer
   - Réutilise les permissions existantes
   - Pas de duplication de logique

4. **Sécurisé** :
   - `IsAuthenticated` garantit que seuls les utilisateurs connectés y accèdent
   - `request.user` assure qu'on accède uniquement à son propre profil

## Principe général

Ce pattern est appliqué dans toute l'API :
- Pas de code superflu
- Réutilisation maximale des fonctionnalités de Django REST Framework
- Sécurité intégrée dès la conception
- Code lisible et maintenable
