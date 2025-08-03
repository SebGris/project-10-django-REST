# 🏗️ Architecture SoftDesk

[← Retour à la documentation](./README.md)

## 📋 Navigation rapide
- [Vue d'ensemble](#vue-densemble)
- [Structure du projet](#structure-du-projet)
- [Architecture technique](#architecture-technique)
- [Modèle de données](./mcd.md)
- [API REST](#api-rest)
- [Sécurité](../security/security-guide.md)

## 🎯 Vue d'ensemble

SoftDesk est une API REST développée avec Django REST Framework, suivant une architecture MVT (Model-View-Template) adaptée pour une API pure.

## 📁 Structure du projet
```
project-10-django-REST/
├── 📁 softdesk_support/          # Configuration principale
│   ├── settings.py              # Configuration Django
│   ├── urls.py                  # Routes principales
│   └── wsgi.py                  # Point d'entrée WSGI
│
├── 📁 users/                    # Application utilisateurs
│   ├── models.py               # Modèle User personnalisé
│   ├── views.py                # ViewSets utilisateurs
│   ├── serializers.py          # Sérialisation JSON
│   └── admin.py                # Interface admin
│
├── 📁 issues/                   # Application principale
│   ├── models.py               # Project, Issue, Comment, Contributor
│   ├── views.py                # ViewSets principaux
│   ├── serializers.py          # Sérialisation JSON
│   ├── permissions.py          # Permissions personnalisées
│   └── admin.py                # Interface admin
│
├── 📁 docs/                     # Documentation complète
├── 📁 tests/                    # Tests unitaires et intégration
└── manage.py                    # Script de gestion Django
```

## 🔧 Architecture technique

### Stack technologique

- **Backend** : Django 5.0 + Django REST Framework
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Authentification** : JWT (Simple JWT)
- **Documentation** : Markdown + Postman
- **Tests** : Django TestCase + unittest

### Patterns utilisés

1. **MVT adapté pour API**
   - Models : Définition des données
   - Views : ViewSets DRF
   - Templates : Remplacés par Serializers

2. **Repository Pattern**
   - ViewSets pour la logique métier
   - Serializers pour la transformation

3. **Permissions personnalisées**
   - IsAuthor : Auteur uniquement
   - IsContributor : Contributeurs du projet

### URLs et routage

```python
# Routes principales
/api/token/                              # Authentification
/api/users/                             # Utilisateurs
/api/projects/                          # Projets

# Routes imbriquées
/api/projects/{id}/contributors/        # Contributeurs
/api/projects/{id}/issues/              # Issues
/api/projects/{id}/issues/{id}/comments/  # Commentaires
```

## 🗄️ Modèle de données

Voir le [Modèle Conceptuel de Données](./mcd.md) pour le détail des entités et relations.

### Entités principales

1. **User** : Utilisateur avec champs RGPD
2. **Project** : Projet de développement
3. **Contributor** : Liaison User-Project
4. **Issue** : Problème/tâche
5. **Comment** : Commentaire sur issue

### Relations clés

- User → auteur de → Project/Issue/Comment
- Project → contient → Contributors/Issues
- Issue → contient → Comments

## 🌐 API REST

### Principes REST respectés

1. **Resources** : URLs représentent des ressources
2. **HTTP Methods** : GET, POST, PUT, DELETE
3. **Stateless** : Pas de session côté serveur
4. **JSON** : Format d'échange unique

### ViewSets et actions

```python
# CRUD automatique avec ModelViewSet
ProjectViewSet → list, create, retrieve, update, destroy

# Actions personnalisées
@action(detail=True, methods=['post'])
def add_contributor(self, request, pk=None):
    # Logique d'ajout de contributeur
```

## 🔒 Sécurité et permissions

Voir le [Guide de sécurité](../security/security-guide.md) pour les détails.

### Niveaux de sécurité

1. **Authentification** : JWT obligatoire
2. **Autorisation** : Permissions par rôle
3. **Validation** : Serializers stricts
4. **Protection** : Rate limiting, CORS

### Matrice des permissions

| Resource | Create | Read | Update | Delete |
|----------|--------|------|--------|--------|
| Project | Authentiques | Contributors | Author | Author |
| Issue | Contributors | Contributors | Author | Author |
| Comment | Contributors | Contributors | Author | Author |

## 🌱 Optimisations Green Code

Voir le [Guide Green Code](../green-code/green-code-guide.md) pour les détails.

### Optimisations implémentées

1. **Requêtes SQL** : select_related/prefetch_related
2. **Pagination** : 20 items par page
3. **Throttling** : Limitation des requêtes
4. **Serializers** : Champs optimisés

## 🧪 Tests et qualité

Voir le [Guide de tests](../tests/testing-guide.md) pour les détails.

### Stratégie de tests

1. **Unitaires** : Models et serializers
2. **Intégration** : ViewSets et permissions
3. **API** : Endpoints et workflows
4. **Performance** : Green Code validé

## 📝 Conventions de code

### Python/Django

- PEP 8 strictement respecté
- Docstrings pour toutes les classes/méthodes
- Type hints quand pertinent
- DRY (Don't Repeat Yourself)

### Nommage

- Models : Singulier (Project, Issue)
- Apps : Pluriel (users, issues)
- ViewSets : NomViewSet
- Serializers : NomSerializer

### Organisation

```python
# Ordre des imports
1. Standard library
2. Django imports
3. Third-party imports
4. Local imports

# Structure des ViewSets
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Logique personnalisée
```

## 🚀 Déploiement

### Environnements

- **Développement** : SQLite, DEBUG=True
- **Staging** : PostgreSQL, DEBUG=False
- **Production** : PostgreSQL, HTTPS, monitoring

### Checklist déploiement

- [ ] Variables d'environnement configurées
- [ ] Base de données PostgreSQL
- [ ] HTTPS activé
- [ ] Static files servis par nginx
- [ ] Logs configurés
- [ ] Monitoring activé
- [ ] Backups automatiques

## 📚 Documentation associée

- [Guide Django](../guides/django/django-guide.md) - Comprendre Django
- [API Guide](../api/api-guide.md) - Documentation API
- [MCD](./mcd.md) - Modèle de données
- [Security](../security/security-guide.md) - Sécurité
- [Green Code](../green-code/green-code-guide.md) - Performance
