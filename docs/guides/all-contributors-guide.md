# 📋 Guide : Obtenir tous les contributeurs de tous les projets

## 🎯 Objectif

Récupérer une liste de tous les contributeurs uniques à travers tous les projets de l'API SoftDesk.

## 🔧 Solutions possibles

### Solution 1 : Via Django Shell (pour les développeurs)

```python
# Dans le shell Django (poetry run python manage.py shell)
from issues.models import Contributor
from django.contrib.auth import get_user_model

User = get_user_model()

# Tous les contributeurs uniques
all_contributors = User.objects.filter(
    id__in=Contributor.objects.values_list('user_id', flat=True).distinct()
)

# Afficher les contributeurs
for user in all_contributors:
    print(f"ID: {user.id}, Username: {user.username}")
    
# Ou avec plus de détails
for contributor in Contributor.objects.select_related('user', 'project'):
    print(f"{contributor.user.username} contribue au projet '{contributor.project.name}'")
```

### Solution 2 : Via l'API existante (méthode manuelle)

1. **Obtenir la liste de tous les projets** :
   ```
   GET {{api_url}}/projects/
   ```

2. **Pour chaque projet, obtenir ses contributeurs** :
   ```
   GET {{api_url}}/projects/{project_id}/contributors/
   ```

3. **Agréger manuellement les résultats**

### Solution 3 : Créer un endpoint personnalisé (si autorisé)

Si vous pouvez modifier le code, ajoutez dans `views.py` :

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_contributors(request):
    """Liste tous les contributeurs uniques avec leurs projets"""
    contributors = User.objects.filter(
        contributor__isnull=False
    ).distinct().annotate(
        projects_count=Count('contributor')
    ).values('id', 'username', 'projects_count')
    
    return Response({
        'count': contributors.count(),
        'results': list(contributors)
    })
```

Et ajouter dans `urls.py` :
```python
path('api/contributors/', all_contributors, name='all-contributors'),
```

## 📊 Exemple de script Python pour agréger

```python
import requests

# Configuration
base_url = "http://127.0.0.1:8000/api"
token = "YOUR_ACCESS_TOKEN"
headers = {"Authorization": f"Bearer {token}"}

# 1. Obtenir tous les projets
projects_response = requests.get(f"{base_url}/projects/", headers=headers)
projects = projects_response.json()['results']

# 2. Collecter tous les contributeurs
all_contributors = {}

for project in projects:
    contributors_url = f"{base_url}/projects/{project['id']}/contributors/"
    contributors_response = requests.get(contributors_url, headers=headers)
    contributors = contributors_response.json()['results']
    
    for contributor in contributors:
        user_id = contributor['user']['id']
        username = contributor['user']['username']
        
        if user_id not in all_contributors:
            all_contributors[user_id] = {
                'username': username,
                'projects': []
            }
        
        all_contributors[user_id]['projects'].append({
            'id': project['id'],
            'name': project['name']
        })

# 3. Afficher les résultats
print(f"Total contributeurs uniques : {len(all_contributors)}")
for user_id, data in all_contributors.items():
    print(f"\n{data['username']} (ID: {user_id})")
    print(f"  Contribue à {len(data['projects'])} projet(s):")
    for project in data['projects']:
        print(f"    - {project['name']} (ID: {project['id']})")
```

## 🚀 Utilisation avec cURL

```bash
# 1. Obtenir le token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "SoftDesk2025!"}' \
  | jq -r '.access')

# 2. Obtenir tous les projets
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8000/api/projects/ | jq

# 3. Pour chaque projet, obtenir les contributeurs
for id in 105 106; do
  echo "Contributeurs du projet $id:"
  curl -H "Authorization: Bearer $TOKEN" \
    http://127.0.0.1:8000/api/projects/$id/contributors/ | jq
done
```

## 💡 Astuce Postman

Créez une collection Postman avec un script de pré-requête qui :
1. Récupère tous les projets
2. Itère sur chaque projet pour obtenir ses contributeurs
3. Compile une liste unique

```javascript
// Dans l'onglet "Pre-request Script" de Postman
pm.sendRequest({
    url: pm.environment.get('api_url') + '/projects/',
    method: 'GET',
    header: {
        'Authorization': 'Bearer ' + pm.environment.get('access_token')
    }
}, function (err, response) {
    if (!err) {
        const projects = response.json().results;
        pm.environment.set('all_projects', JSON.stringify(projects));
    }
});
```

## 📋 Résultat attendu

Une liste consolidée comme :
```json
{
  "contributors": [
    {
      "id": 34,
      "username": "admin",
      "projects_count": 2,
      "projects": ["Projet Test", "Projet Comptable"]
    },
    {
      "id": 199,
      "username": "SEB",
      "projects_count": 1,
      "projects": ["Projet Comptable"]
    },
    {
      "id": 200,
      "username": "john__1754220224",
      "projects_count": 1,
      "projects": ["Projet Test"]
    }
  ]
}
```

## ⚡ Performance

Pour de grandes quantités de données, préférez :
- La solution Django Shell pour une exécution côté serveur
- Un endpoint personnalisé avec pagination
- Une vue SQL si vous avez accès à la base de données

---

**Note** : L'API SoftDesk actuelle ne propose pas d'endpoint direct pour cette fonctionnalité. Les solutions proposées permettent d'obtenir le résultat souhaité avec les outils disponibles.
