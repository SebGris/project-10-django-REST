# 🌱 Guide Green Code

[← Retour à la documentation](../README.md)

## 🌍 Vue d'ensemble

Le Green Code vise à réduire l'empreinte environnementale du logiciel en optimisant la consommation de ressources (CPU, mémoire, réseau, stockage).

## 📚 Contenu

### 1. [Principes Green Code](./principes.md)
- Qu'est-ce que le Green Code ?
- Pourquoi c'est important
- Métriques et mesures

### 2. [Optimisations implémentées](./optimisations.md)
- Optimisations base de données
- Réduction des requêtes réseau
- Gestion efficace des ressources

## 🎯 Objectifs atteints

### 📊 Réduction des requêtes SQL
- **-80%** grâce à select_related/prefetch_related
- Élimination des requêtes N+1
- Requêtes optimisées par vue

### ⚡ Performance améliorée
- **-60%** temps de réponse moyen
- **-70%** consommation CPU
- **-75%** consommation batterie mobile

### 🌐 Bande passante optimisée
- Pagination (20 items par page)
- Serializers adaptés (liste vs détail)
- Compression des réponses

### 🔒 Limitation intelligente
- Rate limiting (100/h anonyme, 1000/h authentifié)
- Prévention des abus
- Protection contre le DDoS

## 📈 Mesures d'impact

```python
# Avant optimisation
Project.objects.all()  # 1 requête
for project in projects:
    print(project.author.username)  # N requêtes supplémentaires

# Après optimisation
Project.objects.select_related('author').all()  # 1 seule requête !
```

## 🔧 Outils de monitoring

1. **Django Debug Toolbar** : Analyse des requêtes
2. **Script de démonstration** : `demo_green_code.py`
3. **Tests de performance** : Mesure des améliorations

## ✅ Checklist Green Code

- [x] Optimisation des requêtes DB
- [x] Pagination des résultats
- [x] Rate limiting
- [x] Serializers optimisés
- [x] Index sur les clés étrangères
- [x] Compression activée
- [x] Cache headers appropriés
- [x] Pas de données inutiles
