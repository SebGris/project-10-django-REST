# 📚 Documentation SoftDesk API

## 🎯 Fonctionnalités de l'application

SoftDesk est une API REST pour la gestion collaborative de projets avec système de tickets. Voici les principales fonctionnalités :

### 👤 Gestion des utilisateurs

### 📋 Gestion des projets
- Un utilisateur peut créer un projet. Il en devient l'auteur et le contributeur. [Voir l'implémentation](./projets/creation-projet-implementation.md)

### 🐛 Création des tâches et des problèmes

### 💬 Création des commentaires pour faciliter la communication

### ℹ️ Informations complémentaires

### 📄 Mise en place de la pagination

## 📋 Navigation rapide

### 🚀 Démarrage
- [Installation et configuration](../README.md)
- [Guide Django](./guides/django/django-guide.md)
- [Architecture du projet](./architecture/architecture.md)

### 📖 Guides API
- [Documentation complète API](./api/api-guide.md)
- [Guide des tests API](./api/api-testing-complete-guide.md)
- [Tests API utilisateurs](./api/users-api-testing.md)
- [Guide Issues/Comments](./api/issue-comment-api-guide.md)

### 🔧 Concepts techniques

#### Django
- [Guide Django complet](./guides/django/django-guide.md)
- [Raw strings Python (r'')](./guides/django/raw-strings-guide.md)
- [Get_or_create et defaults](./guides/django/get-or-create-defaults.md)

#### Django REST Framework
- [ModelViewSet DRF](./guides/djangorestframework/modelviewset-guide.md)
- [DefaultRouter expliqué](./guides/djangorestframework/defaultrouter-guide.md)
- [Routes imbriquées](./guides/djangorestframework/nested-router-guide.md)

### 🌱 Green Code & Performance
- [Guide Green Code](./green-code/green-code-guide.md)
- [Rapport de conformité Green Code](./green-code/green-code-compliance-report.md)
- [Problème N+1 expliqué](./performance/n-plus-1-explained.md)

### 🔒 Sécurité & Conformité
- [Guide de sécurité](./security/security-guide.md)
- [Conformité RGPD](./security/rgpd-compliance.md)

### 🧪 Tests & Dépannage
- [Guide de tests](./tests/testing-guide.md)
- [Guide de dépannage](./support/troubleshooting.md)

### 🔧 Maintenance
- [Instructions de migration](./support/migration-instructions.md)

### 📊 Références
- [Modèle conceptuel de données](./architecture/mcd.md)

## 🎯 Par où commencer ?

| Si vous voulez... | Consultez |
|-------------------|-----------|
| Installer le projet | [README principal](../README.md) |
| Comprendre l'architecture | [architecture.md](./architecture/architecture.md) |
| Utiliser l'API | [api-guide.md](./api/api-guide.md) |
| Tester l'API | [Collection Postman](./postman/postman-guide.md) |
| Résoudre un problème | [troubleshooting.md](./support/troubleshooting.md) |

## 📁 Organisation des fichiers

```
docs/
├── README.md                        # Ce fichier (sommaire)
├── api/                            # Documentation API
│   ├── api-guide.md
│   ├── api-testing-complete-guide.md
│   ├── issue-comment-api-guide.md
│   └── users-api-testing.md
├── architecture/                   # Architecture et conception
│   ├── architecture.md
│   └── mcd.md
├── guides/                        # Guides techniques
│   ├── README.md                  # Index des guides
│   ├── django/                    # Guides Django purs
│   │   ├── README.md
│   │   ├── django-guide.md
│   │   ├── raw-strings-guide.md
│   │   └── get-or-create-defaults.md
│   └── djangorestframework/       # Guides DRF
│       ├── README.md
│       ├── defaultrouter-guide.md
│       ├── modelviewset-guide.md
│       └── nested-router-guide.md
├── performance/                   # Performance et Green Code
│   ├── green-code-guide.md
│   ├── green-code-compliance-report.md
│   └── n-plus-1-explained.md
├── security/                      # Sécurité et conformité
│   ├── rgpd-compliance.md
│   └── security-guide.md
├── tests/                         # Tests et qualité
│   └── testing-guide.md
├── support/                       # Support et dépannage
│   ├── troubleshooting.md
│   └── migration-instructions.md
└── postman/                       # Collections Postman
    └── postman-guide.md
```

## 📝 Conventions de documentation

- **Fichiers en minuscules** : Tous les guides sauf README
- **Organisation par thème** : Dossiers spécialisés
- **Emojis** : Navigation visuelle rapide
- **Tables** : Résumés et références rapides
