# 📚 Documentation SoftDesk API

## 📋 Navigation rapide

### 🚀 Démarrage
- [Installation et configuration](../README.md)
- [Guide Django](./guides/django-guide.md)
- [Architecture du projet](./architecture/architecture.md)

### 📖 Guides API
- [Documentation complète API](./api/api-guide.md)
- [Guide des tests API](./api/api-testing-complete-guide.md)
- [Tests API utilisateurs](./api/users-api-testing.md)
- [Guide Issues/Comments](./api/issue-comment-api-guide.md)

### 🔧 Concepts techniques
- [ModelViewSet DRF](./guides/modelviewset-guide.md)
- [DefaultRouter expliqué](./guides/defaultrouter-guide.md)
- [Raw strings Python (r'')](./guides/raw-strings-guide.md)
- [Routes imbriquées](./guides/nested-router-guide.md)
- [Problème N+1 expliqué](./performance/n-plus-1-explained.md)
- [Get_or_create et defaults](./developpement/get-or-create-defaults.md)

### 🌱 Green Code & Performance
- [Guide Green Code](./performance/green-code-guide.md)
- [Rapport de conformité Green Code](./performance/green-code-compliance-report.md)

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
│   ├── defaultrouter-guide.md
│   ├── django-guide.md
│   ├── modelviewset-guide.md
│   ├── nested-router-guide.md
│   └── raw-strings-guide.md
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
│   └── migration-instructions.md  # Instructions de migration
├── postman/                       # Collections Postman
│   └── postman-guide.md
└── developpement/                 # Guides de développement
    ├── README.md
    └── get-or-create-defaults.md
```

## 📝 Conventions de documentation

- **Fichiers en minuscules** : Tous les guides sauf README
- **Organisation par thème** : Dossiers spécialisés
- **Emojis** : Navigation visuelle rapide
- **Tables** : Résumés et références rapides
- **Emojis** : Navigation visuelle rapide
- **Tables** : Résumés et références rapides
