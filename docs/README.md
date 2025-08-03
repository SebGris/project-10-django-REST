# 📚 Documentation SoftDesk API

## 🎯 Fonctionnalités principales

SoftDesk est une API REST permettant la gestion collaborative de projets avec un système de tickets. Voici ses principales fonctionnalités :

### 👤 Gestion des utilisateurs
- Inscription avec validation RGPD (âge minimum 15 ans)
- Authentification JWT avec tokens de rafraîchissement
- Gestion du profil et des préférences de confidentialité

### 📋 Gestion des projets
- Création de projets par les utilisateurs (l'auteur devient automatiquement contributeur)
- Gestion des contributeurs par projet
- Types de projets : back-end, front-end, iOS, Android

### 🐛 Gestion des tâches et problèmes
- Création, modification et suivi des tickets (issues)
- Priorités : LOW, MEDIUM, HIGH
- Tags : BUG, FEATURE, TASK
- Statuts : To Do, In Progress, Finished

### 💬 Commentaires
- Ajout de commentaires pour faciliter la communication entre les membres du projet
- Historique complet des échanges sur chaque issue

### ℹ️ Informations complémentaires

#### Définition des auteurs
- Chaque ressource (hors utilisateur) possède un auteur
- Seul l'auteur peut modifier ou supprimer sa ressource ; les autres utilisateurs ont un accès en lecture seule

#### 📄 Pagination
- Mise en place de la pagination sur les listes de ressources pour optimiser la navigation

## 📋 Navigation rapide

### 🚀 Démarrage
- [Installation et configuration](../README.md)
- [Architecture du projet](./architecture/architecture.md)

### 📖 Guides API
- [Documentation complète de l'API](./api/api-guide.md)
- [Choix de conception de l'API](./api/api-design.md)
- [Guide des tests API](./api/api-testing-complete-guide.md)
- [Tests API utilisateurs](./api/users-api-testing.md)
- [Guide Issues/Comments](./api/issue-comment-api-guide.md)

### 🔧 Concepts techniques

#### Django
- [Guide Django complet](./guides/django/django-guide.md)
- [Raw strings Python (r'')](./guides/django/raw-strings-guide.md)
- [get_or_create et defaults](./guides/django/get-or-create-defaults.md)

#### Django REST Framework
- [ModelViewSet DRF](./guides/djangorestframework/modelviewset-guide.md)
- [DefaultRouter expliqué](./guides/djangorestframework/defaultrouter-guide.md)
- [Routes imbriquées](./guides/djangorestframework/nested-router-guide.md)
- [Décorateur @action](./guides/djangorestframework/action-decorator-guide.md)

### 🌱 Green Code & Performance
- [Guide Green Code](./green-code/green-code-guide.md)
- [Rapport de conformité Green Code](./green-code/green-code-compliance-report.md)
- [Problème N+1 expliqué](./performance/n-plus-1-explained.md)

### 🔒 Sécurité & Conformité
- [Guide de sécurité](./security/security-guide.md)
- [Conformité RGPD](./security/rgpd-compliance.md)

### 🔧 Maintenance
- [Instructions de migration](./support/migration-instructions.md)
- [Guide de dépannage](./support/troubleshooting.md)

### 📊 Références
- [Modèle conceptuel de données](./architecture/mcd.md)
- [Collection Postman](./postman/postman-guide.md)
- [Guide tous contributeurs](./guides/all-contributors-guide.md)

## 🎯 Par où commencer ?

| Objectif                  | Ressource recommandée                          |
|---------------------------|------------------------------------------------|
| Installer le projet       | [README principal](../README.md)               |
| Comprendre l'architecture | [architecture.md](./architecture/architecture.md) |
| Utiliser l'API            | [api-guide.md](./api/api-guide.md)             |
| Tester l'API              | [Collection Postman](./postman/softdesk-api-collection.json) |
| Résoudre un problème      | [troubleshooting.md](./support/troubleshooting.md) |

## 📁 Organisation des fichiers
```
docs/
├── README.md                        # Ce fichier (sommaire)
├── api/                             # Documentation API
│   ├── api-guide.md
│   ├── api-design.md
│   ├── api-testing-complete-guide.md
│   ├── issue-comment-api-guide.md
│   └── users-api-testing.md
├── architecture/                    # Architecture et conception
│   ├── architecture.md
│   └── mcd.md
├── guides/                          # Guides techniques
│   ├── README.md                    # Index des guides
│   ├── django/                      # Guides Django purs
│   │   ├── README.md
│   │   ├── django-guide.md
│   │   ├── raw-strings-guide.md
│   │   └── get-or-create-defaults.md
│   └── djangorestframework/         # Guides DRF
│       ├── README.md
│       ├── defaultrouter-guide.md
│       ├── modelviewset-guide.md
│       └── nested-router-guide.md
├── performance/                     # Performance et Green Code
│   ├── green-code-guide.md
│   ├── green-code-compliance-report.md
│   └── n-plus-1-explained.md
├── security/                        # Sécurité et conformité
│   ├── rgpd-compliance.md
│   └── security-guide.md
├── support/                         # Support et dépannage
│   ├── troubleshooting.md
│   └── migration-instructions.md
└── postman/                         # Collections Postman
    └── postman-guide.md
```

## 📝 Conventions de documentation

- **Fichiers en minuscules** : Tous les guides sauf README
- **Organisation par thème** : Dossiers spécialisés
- **Emojis** : Navigation visuelle rapide
- **Tableaux** : Résumés et références rapides
