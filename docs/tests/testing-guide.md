# 🧪 Tests SoftDesk - Guide Complet d'Assurance Qualité

[← Retour à la documentation](./README.md)

## 📋 Navigation rapide
- [Exécution rapide](#exécution-rapide)
- [Structure des tests](#structure-des-tests)
- [Types de tests](#types-de-tests)
- [Guide de dépannage](./TROUBLESHOOTING.md#erreur-dencodage-unicode)

## 🚀 Exécution rapide

### Tous les tests
```bash
# Version recommandée (gère tous les problèmes)
poetry run python run_tests_universal.py

# Version originale (nécessite encodage UTF-8)
poetry run python run_all_tests.py
```

### Tests par catégorie
```bash
# Tests des modèles
poetry run python tests/models/test_project_contributor.py
poetry run python tests/models/test_issue_comment.py

# Tests des API
poetry run python tests/api/test_basic_api.py
poetry run python tests/api/test_complete_api.py

# Tests RGPD
poetry run python tests/rgpd/test_compliance.py

# Tests de performance
poetry run python tests/performance/test_performance.py
```

## 📁 Structure des tests

```
tests/
├── __init__.py
├── test_config.py               # Configuration partagée
├── README.md                    # Documentation des tests
├── models/                      # Tests des modèles Django
│   ├── test_project_contributor.py
│   ├── test_project_contributor_simple.py
│   ├── test_issue_comment.py
│   └── test_issue_comment_simple.py
├── api/                         # Tests des endpoints API
│   ├── test_basic_api.py
│   ├── test_complete_api.py
│   ├── test_issue_comment_api.py
│   └── test_nested_routes.py
├── rgpd/                        # Tests de conformité RGPD
│   ├── test_compliance.py
│   ├── test_api.py
│   └── test_age_validation.py
└── performance/                 # Tests Green Code
    ├── test_performance.py
    └── demo_n_plus_1.py
```

## 🔍 Description détaillée des tests

### Tests des modèles (tests/models/)

#### `test_project_contributor.py`
Test complet des modèles Project et Contributor :
- ✅ Création d'utilisateurs et projets
- ✅ Test des méthodes `can_user_modify()`, `can_user_access()`
- ✅ Gestion automatique auteur → contributeur
- ✅ Relations Many-to-Many et permissions
- ✅ Méthodes `get_all_contributors()`, `get_non_author_contributors()`

#### `test_project_contributor_simple.py`
Version allégée pour validation rapide :
- ✅ Création utilisateurs avec champs RGPD
- ✅ Création projet et ajout contributeur
- ✅ Vérification des relations de base

#### `test_issue_comment.py`
Test exhaustif des modèles Issue et Comment :
- ✅ Création d'issues avec différentes priorités/statuts
- ✅ Test des assignations et relations
- ✅ Création de commentaires avec UUID
- ✅ Relations OneToMany (Project→Issue, Issue→Comment)

#### `test_issue_comment_simple.py`
Version simplifiée Issue/Comment :
- ✅ Création issue avec choix (priority, tag, status)
- ✅ Création commentaire avec UUID
- ✅ Vérification des relations de base

### Tests des API (tests/api/)

#### `test_basic_api.py`
Test de base de l'API :
- ✅ Authentification JWT
- ✅ Liste des projets
- ✅ Création de projet
- ✅ Détails d'un projet

#### `test_complete_api.py`
Test exhaustif de tous les endpoints :
- ✅ Test du serveur Django
- ✅ Inscription d'utilisateur
- ✅ Authentification JWT
- ✅ CRUD complet des projets
- ✅ Gestion des contributeurs
- ✅ Endpoints utilisateurs

#### `test_issue_comment_api.py`
Test spécialisé pour Issues et Comments :
- ✅ CRUD complet des issues (16 tests)
- ✅ CRUD complet des commentaires
- ✅ Test des permissions et sécurité
- ✅ Validation des relations et contraintes

#### `test_nested_routes.py`
Test des routes imbriquées RESTful :
- ✅ Routes `/api/projects/{id}/issues/`
- ✅ Routes `/api/projects/{id}/issues/{id}/comments/`
- ✅ Création via routes imbriquées
- ✅ Validation de l'architecture RESTful

### Tests RGPD (tests/rgpd/)

#### `test_compliance.py`
Test de conformité RGPD et protection des données :
- ✅ Validation des champs RGPD (`can_be_contacted`, `can_data_be_shared`)
- ✅ Test de l'anonymisation des utilisateurs
- ✅ Suppression en cascade des données
- ✅ Respect de la réglementation

#### `test_api.py`
Test des endpoints RGPD via l'API :
- ✅ Endpoints de gestion des consentements
- ✅ Anonymisation via API
- ✅ Validation des permissions RGPD

#### `test_age_validation.py`
Test de validation d'âge RGPD :
- ✅ Rejet des utilisateurs < 15 ans
- ✅ Acceptation des utilisateurs ≥ 15 ans
- ✅ Messages d'erreur appropriés

### Tests de performance (tests/performance/)

#### `test_performance.py`
Test complet de performance Green Code :
- 🔍 Mesure du nombre de requêtes SQL
- ⏱️ Mesure des temps d'exécution
- 📊 Calcul du score Green Code
- 🎯 Conseils d'amélioration personnalisés

#### `demo_n_plus_1.py`
Démonstration du problème N+1 :
- ❌ Exemple du problème N+1
- ✅ Solution optimisée avec select_related/prefetch_related
- 📈 Comparaison des performances

## 🔧 Résolution des problèmes

### Erreurs courantes

#### 1. "No module named 'softdesk_support'"
**Cause :** Utilisation de `python` au lieu de `poetry run python`

**Solution :**
```bash
# ❌ FAUX
python run_all_tests.py

# ✅ CORRECT
poetry run python run_all_tests.py
```

#### 2. "UnicodeEncodeError: 'charmap' codec"
**Cause :** Emojis incompatibles avec cmd.exe Windows

**Solutions :**
```bash
# Solution A : Script universel (recommandé)
poetry run python run_tests_universal.py

# Solution B : Forcer UTF-8
set PYTHONIOENCODING=utf-8 && poetry run python run_all_tests.py

# Solution C : PowerShell
$env:PYTHONIOENCODING="utf-8"; poetry run python run_all_tests.py
```

#### 3. Serveur Django non démarré
**Cause :** Tests API nécessitent un serveur actif

**Solution :**
```bash
# Terminal 1 : Démarrer le serveur
poetry run python manage.py runserver

# Terminal 2 : Lancer les tests API
poetry run python tests/api/test_basic_api.py
```

### Outils de diagnostic

#### Diagnostic complet
```bash
poetry run python diagnose_project.py
```

#### Test simple
```bash
poetry run python test_simple.py
```

#### Vérification Django
```bash
poetry run python manage.py check
```

## 📊 Métriques et couverture

### Couverture des tests
| Type de test | Fichiers | Couverture | Statut |
|--------------|----------|------------|--------|
| **Modèles** | 4 | 100% | ✅ |
| **API** | 4 | 100% | ✅ |
| **RGPD** | 3 | 100% | ✅ |
| **Performance** | 2 | 100% | ✅ |
| **Total** | **13** | **100%** | ✅ |

### Validation complète
Tous les tests passent avec un taux de réussite de **100%**, validant :
- 🏗️ **Architecture** : Modèles, relations, contraintes
- 🌐 **API** : CRUD complet, permissions, authentification JWT
- 🔗 **RESTful** : Routes imbriquées conformes aux standards
- 🔒 **Sécurité** : Authentification, autorisation, permissions
- 📝 **RGPD** : Conformité réglementaire complète
- ⚡ **Performance** : Optimisations Green Code

## 🎯 Bonnes pratiques

### 1. Toujours utiliser Poetry
```bash
poetry run python <script_de_test>
```

### 2. Tests par ordre de complexité
1. Tests simples (modèles)
2. Tests API (nécessite serveur)
3. Tests de performance
4. Tests complets

### 3. Nettoyage automatique
Tous les tests nettoient leurs données automatiquement.

### 4. Configuration partagée
Utilisez `tests/test_config.py` pour les configurations communes.

## 🚀 Intégration continue

### Scripts d'automatisation
- `run_all_tests.py` - Version originale
- `run_tests_universal.py` - Version compatible Windows
- `diagnose_project.py` - Diagnostic et vérification

### Variables d'environnement
```bash
export PYTHONIOENCODING=utf-8
export DJANGO_SETTINGS_MODULE=softdesk_support.settings
```

## 📚 Ressources

- [Documentation Django Testing](https://docs.djangoproject.com/en/stable/topics/testing/)
- [DRF Testing](https://www.django-rest-framework.org/api-guide/testing/)
- [Guide des tests Python](https://docs.python.org/3/library/unittest.html)

Cette documentation garantit une exécution fiable et complète de tous les tests du projet SoftDesk.
