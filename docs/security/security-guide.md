# 🛡️ Sécurité SoftDesk - Guide de Protection et Authentification

[← Retour à la documentation](../README.md)

## 📋 Navigation rapide
- [Vue d'ensemble](#vue-densemble-de-la-sécurité)
- [Authentification JWT](#authentification-jwt)
- [Permissions](#système-de-permissions-granulaires)
- [Protection contre les attaques](#protection-contre-les-attaques)
- [Conformité RGPD](./rgpd-compliance.md)
- [Tests de sécurité](#tests-de-sécurité)

## 🔒 Vue d'ensemble de la sécurité

Le projet SoftDesk implémente une architecture de sécurité robuste basée sur les meilleures pratiques Django et Django REST Framework, avec des mesures spécifiques pour la protection des données et la prévention des attaques.

## 🔐 Authentification et autorisation

### 1. Authentification JWT

**Configuration sécurisée :**
```python
# settings/security.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Avantages sécuritaires :**
- ✅ Tokens à durée de vie limitée
- ✅ Rotation automatique des tokens
- ✅ Blacklist des anciens tokens
- ✅ Algorithme de signature sécurisé

### 2. Système de permissions granulaires

### Classes de permissions utilisées

1. **IsAuthenticated** (Django REST Framework)
   - Vérifie que l'utilisateur est authentifié
   - Appliquée globalement sur tous les endpoints protégés

2. **IsProjectAuthorOrContributor** (Custom)
   ```python
   class IsProjectAuthorOrContributor(permissions.BasePermission):
       """
       Permission pour les projets : seuls les contributeurs peuvent accéder,
       seul l'auteur peut modifier/supprimer
       """
       def has_object_permission(self, request, view, obj):
           # Seuls les contributeurs peuvent accéder au projet
           if not obj.contributors.filter(user=request.user).exists():
               return False
           
           # Pour les modifications, seul l'auteur peut modifier
           if view.action in ['update', 'partial_update', 'destroy']:
               return obj.author == request.user
           
           # Pour la lecture (tous les contributeurs)
           return True
   ```

### Règles de permissions par ressource

| Ressource | Création | Lecture | Modification | Suppression |
|-----------|----------|---------|--------------|-------------|
| User | Public (inscription) | Authentifié | Propriétaire | Admin |
| Project | Authentifié | Authentifié | Auteur | Auteur |
| Issue | Authentifié | Authentifié | Auteur | Auteur |
| Comment | Authentifié | Authentifié | Auteur | Auteur |
| Contributor | Auteur du projet | Authentifié | - | - |

### 3. Protection des mots de passe

**Validation forte :**
```python
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8,}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Chiffrement :**
- Algorithme : PBKDF2 avec SHA256
- Iterations : 216 000 (Django 4.2+)
- Salt unique par mot de passe

## 🚫 Protection contre les attaques

### 1. Limitation du taux de requêtes (Rate Limiting)

**Configuration :**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',     # Utilisateurs anonymes
        'user': '1000/hour',    # Utilisateurs authentifiés
        'login': '5/minute',    # Tentatives de connexion
    }
}
```

**Protection contre :**
- 🛡️ Attaques par déni de service (DoS)
- 🛡️ Brute force sur l'authentification
- 🛡️ Scraping excessif des données

### 2. Protection CSRF

**Activation :**
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protection CSRF
    # ...
]
```

**Exemption pour l'API :**
```python
# Les vues API utilisent TokenAuthentication, pas les sessions
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

### 3. Protection contre l'injection SQL

**ORM Django sécurisé :**
```python
# ✅ Sécurisé - Utilisation de l'ORM
projects = Project.objects.filter(author=request.user)

# ✅ Sécurisé - Requête paramétrisée
projects = Project.objects.extra(
    where=["title LIKE %s"],
    params=[f"%{search_term}%"]
)

# ❌ Vulnérable - Évité dans le projet
# Project.objects.extra(where=[f"title LIKE '{search_term}'"])
```

### 4. Protection XSS

**Échappement automatique :**
```python
# Django échappe automatiquement les données dans les templates
# Les vues API sérialisent en JSON (pas de HTML)

# Validation des entrées
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        
    def validate_title(self, value):
        # Validation supplémentaire si nécessaire
        return value
```

## 🔍 Validation et filtrage des données

### 1. Serializers sécurisés

**Validation stricte :**
```python
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    age = serializers.IntegerField(min_value=15)  # Conformité RGPD
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'age', 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)  # Chiffrement automatique
        user.save()
        return user
```

### 2. Filtrage des champs sensibles

**Exclusion des données sensibles :**
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'is_staff', 'is_superuser', 'user_permissions')
        read_only_fields = ('id', 'date_joined', 'last_login')
```

## 🌐 Sécurité réseau et CORS

### 1. Configuration CORS sécurisée

```python
# En production
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# En développement
CORS_ALLOW_ALL_ORIGINS = True  # Uniquement en dev
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

### 2. Headers de sécurité

```python
# Security middleware
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# En production
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## 🔧 Configuration de sécurité Django

### 1. Settings de production

```python
# settings/production.py
import os
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

# Base de données sécurisée
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Clé secrète depuis les variables d'environnement
SECRET_KEY = os.getenv('SECRET_KEY')

# Logging sécurisé
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}
```

### 2. Variables d'environnement

```env
# .env (ne jamais committer)
SECRET_KEY=your-super-secret-key-here
DB_NAME=softdesk_prod
DB_USER=softdesk_user
DB_PASSWORD=super-secure-password
DB_HOST=localhost
DB_PORT=5432
DJANGO_SETTINGS_MODULE=config.settings.production
```

## 🧪 Tests de sécurité

### 1. Test d'authentification

```bash
# Test sans token
curl http://127.0.0.1:8000/api/projects/
# Réponse attendue : 401 Unauthorized

# Test avec token invalide
curl -H "Authorization: Bearer invalid_token" \
  http://127.0.0.1:8000/api/projects/
# Réponse attendue : 401 Unauthorized

# Test avec token valide
curl -H "Authorization: Bearer YOUR_VALID_TOKEN" \
  http://127.0.0.1:8000/api/projects/
# Réponse attendue : 200 OK avec données
```

### 2. Test des permissions

```bash
# Test d'accès à un projet non autorisé
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/projects/999/
# Réponse attendue : 404 Not Found (ou 403 Forbidden)

# Test de modification par non-auteur
curl -X PUT http://127.0.0.1:8000/api/projects/1/ \
  -H "Authorization: Bearer OTHER_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Hack attempt"}'
# Réponse attendue : 403 Forbidden
```

### 3. Test de rate limiting

```bash
# Script de test de limite de taux
for i in {1..10}; do
  curl -X POST http://127.0.0.1:8000/api/auth/login/ \
    -H "Content-Type: application/json" \
    -d '{"username": "test", "password": "wrong"}'
  echo "Tentative $i"
done
# Après 5 tentatives : 429 Too Many Requests
```

### 4. Tests automatisés de sécurité

```python
# tests/security/test_authentication.py
class SecurityTestCase(TestCase):
    def test_unauthenticated_access_denied(self):
        """Test que l'accès non authentifié est refusé"""
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 401)
    
    def test_invalid_token_rejected(self):
        """Test que les tokens invalides sont rejetés"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 401)
    
    def test_unauthorized_modification_blocked(self):
        """Test que les modifications non autorisées sont bloquées"""
        # Code de test...
```

## 📊 Monitoring et logs de sécurité

### 1. Événements à surveiller

- 🚨 Tentatives de connexion échouées répétées
- 🚨 Accès à des ressources non autorisées
- 🚨 Requêtes inhabituelles (volumes, patterns)
- 🚨 Tentatives d'injection (détectées par Django)

### 2. Configuration des logs

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '[{levelname}] {asctime} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/security.log',
            'maxBytes': 1024*1024*5,  # 5 MB
            'backupCount': 5,
            'formatter': 'security',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'softdesk.security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```

## 🔄 Maintenance et mises à jour

### 1. Audit de sécurité régulier

```bash
# Vérification des dépendances
poetry audit

# Mise à jour des dépendances
poetry update

# Scan de sécurité
pip-audit
```

### 2. Checklist de sécurité

- [ ] **Authentification**
  - [ ] JWT configuré avec expiration courte
  - [ ] Rotation des tokens activée
  - [ ] Blacklist fonctionnelle

- [ ] **Autorisation**
  - [ ] Permissions testées pour chaque endpoint
  - [ ] Isolation des données utilisateur
  - [ ] Validation des propriétaires de ressources

- [ ] **Données**
  - [ ] Validation stricte des entrées
  - [ ] Échappement des sorties
  - [ ] Chiffrement des mots de passe

- [ ] **Infrastructure**
  - [ ] HTTPS en production
  - [ ] Headers de sécurité configurés
  - [ ] Rate limiting activé

- [ ] **Conformité**
  - [ ] RGPD respecté
  - [ ] Logs de sécurité configurés
  - [ ] Procédures d'incident définies

## 🚨 Procédures d'incident

### 1. Détection d'une brèche

1. **Isolation immédiate**
   - Bloquer l'accès suspect
   - Révoquer les tokens compromis
   - Analyser les logs

2. **Évaluation**
   - Identifier les données affectées
   - Estimer l'impact
   - Documenter l'incident

3. **Notification**
   - Utilisateurs affectés (si nécessaire)
   - CNIL (si applicable)
   - Équipe technique

4. **Remédiation**
   - Corriger la vulnérabilité
   - Renforcer les mesures
   - Tester les corrections

### 2. Contacts d'urgence

- **Équipe sécurité :** security@softdesk.com
- **Responsable technique :** tech-lead@softdesk.com
- **DPO :** dpo@softdesk.com

Cette architecture de sécurité garantit une protection robuste des données et des utilisateurs tout en maintenant une expérience utilisateur fluide et une conformité réglementaire complète.
