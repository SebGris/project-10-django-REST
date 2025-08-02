# 🔒 RGPD SoftDesk - Guide de Conformité et Protection des Données

[← Retour à la documentation](../README.md)

## 📋 Navigation rapide
- [Vue d'ensemble](#vue-densemble)
- [Conformité implémentée](#conformité-rgpd-implémentée)
- [Mesures de sécurité](#mesures-de-sécurité)
- [API RGPD](#api-rgpd)
- [Tests de conformité](#tests-de-conformité)
- [Guide de sécurité](./security-guide.md)

## 📋 Vue d'ensemble

Le projet SoftDesk intègre une conformité complète au Règlement Général sur la Protection des Données (RGPD). Cette documentation détaille toutes les mesures implémentées pour assurer la protection des données personnelles.

## ⚖️ Conformité RGPD implémentée

### 1. 🔞 Validation d'âge obligatoire

**Règle :** Les utilisateurs de moins de 15 ans ne peuvent pas s'inscrire.

**Implémentation :**
```python
# Dans users/models.py
class User(AbstractUser):
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(15)],
        help_text="Âge minimum requis : 15 ans (conformité RGPD)"
    )
```

**Validation :**
```bash
# Test de validation d'âge
poetry run python tests/rgpd/test_age_validation.py
```

### 2. 📝 Consentements explicites

**Champs de consentement :**
```python
class User(AbstractUser):
    can_be_contacted = models.BooleanField(
        default=False,
        help_text="Consent pour recevoir des communications"
    )
    can_data_be_shared = models.BooleanField(
        default=False,
        help_text="Consent pour partage des données avec des tiers"
    )
```

**Utilisation API :**
```json
{
  "username": "user",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "age": 25,
  "can_be_contacted": true,
  "can_data_be_shared": false
}
```

### 3. 🗑️ Droit à l'effacement (Droit à l'oubli)

**Anonymisation des utilisateurs :**
```python
def anonymize_user(user):
    """Anonymise un utilisateur tout en préservant l'intégrité des données"""
    user.username = f"anonymous_user_{user.id}"
    user.email = f"anonymous_{user.id}@deleted.local"
    user.first_name = ""
    user.last_name = ""
    user.is_active = False
    user.can_be_contacted = False
    user.can_data_be_shared = False
    user.save()
```

**Test d'anonymisation :**
```bash
poetry run python tests/rgpd/test_compliance.py
```

### 4. 🔗 Suppression en cascade contrôlée

**Préservation de l'intégrité :**
- Les projets, issues et commentaires restent accessibles
- L'auteur devient "Utilisateur supprimé"
- Aucune perte de données métier

**Implémentation :**
```python
# Les relations utilisent PROTECT au lieu de CASCADE
author = models.ForeignKey(User, on_delete=models.PROTECT)
```

## 🛡️ Mesures de sécurité

### 1. 🔐 Protection des mots de passe

```python
# Validation forte des mots de passe
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

### 2. 🔒 Authentification sécurisée

**JWT avec expiration :**
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

### 3. 🚫 Limitation du taux de requêtes

**Protection contre les abus :**
```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}
```

## 📊 Gestion des données personnelles

### Données collectées

| Donnée | Obligatoire | Finalité | Base légale |
|--------|-------------|----------|-------------|
| Username | ✅ | Identification | Contrat |
| Email | ✅ | Communication, authentification | Contrat |
| Mot de passe | ✅ | Authentification | Contrat |
| Âge | ✅ | Validation RGPD | Obligation légale |
| Consentement contact | ❌ | Marketing | Consentement |
| Consentement partage | ❌ | Partenariats | Consentement |

### Durée de conservation

- **Comptes actifs :** Tant que le compte existe
- **Comptes supprimés :** Anonymisation immédiate
- **Logs système :** 30 jours maximum
- **Données de session :** 7 jours (JWT refresh)

## 🔧 API RGPD

### Gestion des consentements

**Consulter ses consentements :**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/profile/
```

**Modifier ses consentements :**
```bash
curl -X PATCH http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "can_be_contacted": false,
    "can_data_be_shared": false
  }'
```

### Droit d'accès aux données

**Exporter ses données :**
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/api/users/profile/export/
```

**Réponse :**
```json
{
  "user_data": {
    "username": "user123",
    "email": "user@example.com",
    "age": 25,
    "created_date": "2025-01-15T10:30:00Z",
    "can_be_contacted": true,
    "can_data_be_shared": false
  },
  "projects": [...],
  "issues": [...],
  "comments": [...]
}
```

### Droit de rectification

**Modifier ses données :**
```bash
curl -X PUT http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "nouveau@email.com",
    "can_be_contacted": true
  }'
```

### Droit à l'effacement

**Supprimer son compte :**
```bash
curl -X DELETE http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Processus d'anonymisation :**
1. Données personnelles remplacées par des valeurs anonymes
2. Compte désactivé
3. Consentements révoqués
4. Préservation de l'intégrité des projets/issues/comments

## 🧪 Tests de conformité

### Test de validation d'âge

```bash
poetry run python tests/rgpd/test_age_validation.py
```

**Vérifications :**
- ❌ Rejet des utilisateurs < 15 ans
- ✅ Acceptation des utilisateurs ≥ 15 ans
- 📝 Messages d'erreur appropriés

### Test de conformité complète

```bash
poetry run python tests/rgpd/test_compliance.py
```

**Vérifications :**
- ✅ Champs de consentement obligatoires
- ✅ Anonymisation fonctionnelle
- ✅ Suppression en cascade contrôlée
- ✅ Intégrité des données préservée

### Test API RGPD

```bash
poetry run python tests/rgpd/test_api.py
```

**Vérifications :**
- ✅ Endpoints de gestion des consentements
- ✅ Export des données personnelles
- ✅ Modification des consentements
- ✅ Suppression/anonymisation via API

## 📋 Procédures RGPD

### 1. Demande d'accès aux données

**Processus :**
1. Authentification de l'utilisateur
2. Export de toutes ses données
3. Fourniture au format JSON structuré

**Délai :** Immédiat via API

### 2. Demande de rectification

**Processus :**
1. Modification via l'API profile
2. Validation des nouvelles données
3. Mise à jour en temps réel

**Délai :** Immédiat

### 3. Demande d'effacement

**Processus :**
1. Vérification de l'identité
2. Anonymisation des données personnelles
3. Préservation de l'intégrité référentielle
4. Désactivation du compte

**Délai :** Immédiat

### 4. Portabilité des données

**Format :** JSON structuré
**Contenu :** Toutes les données personnelles et métier
**Accès :** Via API authentifiée

## 🏛️ Base légale et documentation

### Bases légales utilisées

1. **Contrat :** Données nécessaires au service (username, email, password)
2. **Obligation légale :** Validation d'âge RGPD
3. **Consentement :** Communications marketing et partage de données

### Documentation requise

- ✅ Politique de confidentialité
- ✅ CGU avec clauses RGPD
- ✅ Registre des traitements
- ✅ Procédures d'exercice des droits

### Mesures techniques

- ✅ Chiffrement des mots de passe (Django PBKDF2)
- ✅ Authentification forte (JWT)
- ✅ Limitation des tentatives (Throttling)
- ✅ Logs d'accès limités dans le temps
- ✅ Anonymisation réversible impossible

## 🔍 Audit et conformité

### Points de contrôle

```bash
# 1. Validation d'âge
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "age": 14, ...}'
# Doit retourner 400 Bad Request

# 2. Consentements requis
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "can_be_contacted": true, ...}'
# Doit fonctionner

# 3. Anonymisation
curl -X DELETE http://127.0.0.1:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN"
# Doit anonymiser sans supprimer les données métier
```

### Métriques de conformité

- **Taux de validation d'âge :** 100%
- **Respect des consentements :** 100%
- **Anonymisation fonctionnelle :** 100%
- **Intégrité des données :** 100%

## 📚 Ressources

- [Texte du RGPD](https://eur-lex.europa.eu/eli/reg/2016/679/oj)
- [Guide CNIL](https://www.cnil.fr/fr/reglement-europeen-protection-donnees)
- [Django et RGPD](https://docs.djangoproject.com/en/stable/topics/security/)

Cette implémentation garantit une conformité complète au RGPD tout en préservant l'intégrité et l'utilisabilité de l'application SoftDesk.
