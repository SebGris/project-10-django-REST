# 🧹 Guide d'utilisation de Ruff - Linter Python Ultra-Rapide

## 📋 Vue d'ensemble

**Ruff** est un linter et formateur Python ultra-rapide écrit en Rust. Il remplace plusieurs outils (flake8, isort, black, etc.) et est **10-100x plus rapide** que les alternatives traditionnelles.

## ⚙️ Configuration actuelle dans votre projet

Votre projet a déjà Ruff configuré via Poetry :

```toml
# pyproject.toml
[tool.poetry.group.dev.dependencies]
ruff = "^0.12.4"
```

```toml
# ruff.toml
extend-ignore = [
    "E402",  # Module level import not at top of file (nécessaire pour Django setup)
]

[per-file-ignores]
"test_*.py" = ["E402"]
"**/test_*.py" = ["E402"]
```

## 🚀 Comment exécuter Ruff

### 1. **Installation (déjà fait via Poetry)**

```bash
# Vérifier que Ruff est installé
poetry run ruff --version
```

### 2. **Commandes principales**

#### **🔍 Analyser le code (Linting)**
```bash
# Analyser tout le projet
poetry run ruff check

# Analyser un fichier spécifique
poetry run ruff check users/views.py

# Analyser un dossier spécifique
poetry run ruff check users/

# Analyser avec plus de détails
poetry run ruff check --verbose

# Analyser et montrer les erreurs ignorées
poetry run ruff check --show-fixes
```

#### **🔧 Corriger automatiquement**
```bash
# Corriger automatiquement les erreurs possibles
poetry run ruff check --fix

# Corriger de manière interactive (recommandé)
poetry run ruff check --fix --diff

# Corriger seulement certaines règles
poetry run ruff check --fix --select E,W
```

#### **📐 Formater le code**
```bash
# Formater tout le projet
poetry run ruff format

# Formater un fichier spécifique
poetry run ruff format users/views.py

# Prévisualiser les changements sans les appliquer
poetry run ruff format --diff

# Vérifier si le code est bien formaté
poetry run ruff format --check
```

### 3. **Commandes combinées recommandées**

```bash
# Analyse complète + correction automatique
poetry run ruff check --fix && poetry run ruff format

# Vérification avant commit (dry-run)
poetry run ruff check --diff && poetry run ruff format --check

# Pipeline complet de nettoyage
poetry run ruff check --fix --show-fixes && poetry run ruff format
```

## 📊 Exemple d'exécution sur votre projet

### **Analyser votre fichier views.py actuel :**

```bash
# Dans votre terminal
cd "c:\Users\sebas\Documents\OpenClassrooms\Mes_projets\project-10-django-REST"

# Analyser le fichier views.py
poetry run ruff check issues/views.py
```

**Résultat possible :**
```
issues/views.py:45:80: E501 Line too long (95 > 79 characters)
issues/views.py:67:80: E501 Line too long (87 > 79 characters)
issues/views.py:123:1: E302 Expected 2 blank lines, found 1
Found 3 errors.
```

### **Corriger automatiquement :**
```bash
poetry run ruff check issues/views.py --fix
```

## ⚙️ Configuration avancée recommandée

Créons une configuration plus complète pour votre projet Django :

### **Mise à jour du `ruff.toml` :**

```toml
# Configuration Ruff pour SoftDesk API
[tool.ruff]
# Longueur de ligne (Django recommande 88-100)
line-length = 88

# Version Python cible
target-version = "py312"

# Répertoires à exclure
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "migrations",
    ".pytest_cache",
    "node_modules",
]

# Règles à activer
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "S",    # bandit (sécurité)
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "DJ",   # flake8-django
    "UP",   # pyupgrade
]

# Règles à ignorer
ignore = [
    "E402",  # Module level import not at top (Django setup)
    "S101",  # Use of assert (tests)
    "DJ01",  # Django model missing __str__ method
]

# Configuration par fichier
[tool.ruff.per-file-ignores]
"test_*.py" = ["E402", "S101", "S106"]
"**/test_*.py" = ["E402", "S101", "S106"]
"manage.py" = ["E402"]
"*/settings.py" = ["E402", "F405", "F403"]
"*/migrations/*.py" = ["E501", "F401"]

# Configuration isort
[tool.ruff.isort]
known-django = ["django"]
known-first-party = ["softdesk_support", "users", "issues"]
section-order = ["future", "standard-library", "django", "third-party", "first-party", "local-folder"]

# Configuration flake8-django
[tool.ruff.flake8-django]
django-settings-module = "softdesk_support.settings"
```

## 🔧 Intégration dans le workflow

### **1. Script de développement**

Créez un fichier `scripts/lint.bat` :

```batch
@echo off
echo 🧹 Nettoyage du code avec Ruff...
echo.

echo 📋 Analyse des erreurs...
poetry run ruff check --diff

echo.
echo 🔧 Correction automatique...
poetry run ruff check --fix

echo.
echo 📐 Formatage du code...
poetry run ruff format

echo.
echo ✅ Nettoyage terminé !
```

Puis exécutez :
```bash
scripts\lint.bat
```

### **2. Vérification pre-commit**

Script `scripts/check.bat` :
```batch
@echo off
echo 🔍 Vérification du code...

poetry run ruff check
if %errorlevel% neq 0 (
    echo ❌ Erreurs trouvées !
    exit /b 1
)

poetry run ruff format --check
if %errorlevel% neq 0 (
    echo ❌ Code mal formaté !
    exit /b 1
)

echo ✅ Code propre !
```

### **3. Intégration VS Code**

Ajoutez dans `.vscode/settings.json` :
```json
{
    "python.linting.enabled": true,
    "python.linting.ruffEnabled": true,
    "python.formatting.provider": "ruff",
    "python.linting.ruffArgs": ["--config=ruff.toml"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true,
        "source.fixAll": true
    }
}
```

## 📊 Avantages pour votre projet SoftDesk

### **1. Sécurité renforcée :**
```bash
# Détecte les problèmes de sécurité
poetry run ruff check --select S
```

**Exemples détectés :**
- Mots de passe en dur
- Injections SQL potentielles
- Utilisation de `eval()` dangereux

### **2. Conformité Django :**
```bash
# Règles spécifiques Django
poetry run ruff check --select DJ
```

**Exemples détectés :**
- Modèles sans `__str__()`
- Problèmes de migrations
- Mauvaises pratiques Django

### **3. Performance :**
```bash
# Ultra-rapide sur votre projet
time poetry run ruff check  # ~0.1 secondes vs 5+ secondes avec flake8
```

## 🎯 Workflow recommandé

### **Développement quotidien :**
```bash
# 1. Avant de commiter
poetry run ruff check --fix && poetry run ruff format

# 2. Vérification finale
poetry run ruff check && poetry run ruff format --check

# 3. Si tout est OK, commit
git add . && git commit -m "feat: nouvelle fonctionnalité"
```

### **Nettoyage complet du projet :**
```bash
# Pipeline complet
echo "🧹 Nettoyage complet du projet SoftDesk..."
poetry run ruff check --fix --show-fixes
poetry run ruff format
echo "✅ Projet nettoyé !"
```

## 🔍 Commandes utiles pour débuter

### **Démarrage rapide :**
```bash
# 1. Installer/vérifier Ruff
poetry install

# 2. Première analyse
poetry run ruff check

# 3. Correction automatique des erreurs simples
poetry run ruff check --fix

# 4. Formatage du code
poetry run ruff format

# 5. Vérification finale
poetry run ruff check && poetry run ruff format --check
```

### **Commandes par composant :**
```bash
# Analyser seulement les utilisateurs
poetry run ruff check users/

# Analyser seulement les issues
poetry run ruff check issues/

# Analyser les permissions
poetry run ruff check softdesk_support/permissions.py

# Formater un fichier spécifique
poetry run ruff format issues/views.py
```

## 📈 Métriques et rapports

### **Statistiques du projet :**
```bash
# Compter les erreurs par type
poetry run ruff check --statistics

# Rapport détaillé
poetry run ruff check --output-format=json > ruff-report.json
```

## 🏆 Résultat attendu

Après l'exécution de Ruff sur votre projet SoftDesk :

- ✅ **Code formaté** uniformément (PEP 8)
- ✅ **Imports organisés** automatiquement
- ✅ **Erreurs de sécurité** détectées et corrigées
- ✅ **Performance améliorée** (code optimisé)
- ✅ **Conformité Django** respectée
- ✅ **Maintenabilité renforcée**

## 🎯 Commande pour commencer maintenant

```bash
# Exécutez cette commande dans votre terminal :
cd "c:\Users\sebas\Documents\OpenClassrooms\Mes_projets\project-10-django-REST"
poetry run ruff check --fix && poetry run ruff format
```

---

*Guide Ruff - SoftDesk API*  
*Dernière mise à jour : 5 août 2025*  
*Auteur : GitHub Copilot*
