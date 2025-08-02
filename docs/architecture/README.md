# 🏗️ Architecture et Conception

[← Retour à la documentation](../README.md)

## 📋 Vue d'ensemble

Cette section documente l'architecture technique de l'API SoftDesk, les choix de conception et les patterns utilisés.

## 📚 Contenu

### 1. [Structure du projet](./structure-projet.md)
- Organisation des fichiers et dossiers
- Architecture Django REST
- Conventions de nommage

### 2. [Modèles de données](./mcd.md)
- Diagramme ERD
- Relations entre modèles
- Contraintes et validations

### 3. [Architecture générale](./architecture.md)
- Flux d'authentification JWT
- Patterns architecturaux
- Principes de conception

## 🔑 Principes architecturaux

### Separation of Concerns
- **Models** : Logique métier et données
- **Serializers** : Transformation des données
- **Views** : Logique de présentation
- **Permissions** : Logique d'autorisation

### RESTful Design
- Resources identifiées par URLs
- Méthodes HTTP standardisées
- Stateless communication
- JSON comme format d'échange

### Sécurité par design
- Authentification obligatoire
- Permissions granulaires
- Validation des données
- Protection RGPD

## 📊 Diagramme de l'architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│     API     │────▶│  Database   │
│  (Frontend) │     │   (Django)  │     │ (PostgreSQL)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │                    │
       │                    ├── Models           │
       │                    ├── Views            │
       │                    ├── Serializers      │
       │                    └── Permissions      │
       │                                         │
       └────── JWT Authentication ───────────────┘
```

## 🚀 Points clés

1. **API REST pure** : Pas de rendu HTML, JSON uniquement
2. **Authentification JWT** : Stateless et scalable
3. **Permissions personnalisées** : Contrôle fin des accès
4. **Nested routes** : URLs hiérarchiques logiques
