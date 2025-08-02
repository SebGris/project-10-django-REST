# 🐍 Django - Guide de Compréhension Complète

[← Retour à la documentation](../../README.md) | [REST Framework](../djangorestframework/README.md) | [Raw Strings](./raw-strings-guide.md)

## 🎯 **Qu'est-ce que Django ?**

**Django** est un framework web Python qui suit le principe **"Don't Repeat Yourself" (DRY)** et facilite le développement d'applications web robustes et sécurisées.

**Créé par :** Adrian Holovaty et Simon Willison (2005)  
**Philosophie :** "Le framework web pour les perfectionnistes sous pression"  
**Utilisé par :** Instagram, Pinterest, Mozilla, National Geographic, Spotify...

## 🏗️ **Architecture Django : Le Pattern MVT**

Django utilise le pattern **Model-View-Template (MVT)** :

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     MODEL       │    │      VIEW       │    │    TEMPLATE     │
│                 │    │                 │    │                 │
│ • Base de       │    │ • Logique       │    │ • Présentation  │
│   données       │◄──►│   métier        │◄──►│   HTML/CSS      │
│ • Validation    │    │ • Traitement    │    │ • Interface     │
│ • Relations     │    │ • API REST      │    │   utilisateur   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📋 **Dans votre projet SoftDesk :**

**MODELS** (`models.py`) :
```python
class Project(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Définit la structure des données
```

**VIEWS** (`views.py`) :
```python
class ProjectViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        # Logique métier : qui peut voir quels projets
        return Project.objects.filter(contributors__user=self.request.user)
```

**"TEMPLATES"** → **API JSON** (pas de HTML) :
```json
{
    "id": 1,
    "name": "Mon Projet",
    "author": {"username": "admin"}
}
```

## 🗂️ **Structure d'un Projet Django**

### **Votre projet SoftDesk expliqué :**

```
project-10-django-REST/
│
├── 📁 softdesk_support/          # 🏢 PROJET PRINCIPAL
│   ├── settings.py               # ⚙️ Configuration globale
│   ├── urls.py                   # 🛣️ Routes principales
│   └── wsgi.py                   # 🚀 Déploiement
│
├── 📁 users/                     # 📱 APPLICATION "Utilisateurs"
│   ├── models.py                 # 👤 Modèle User personnalisé
│   ├── views.py                  # 🔧 API des utilisateurs
│   ├── serializers.py            # 📤 Conversion JSON
│   └── admin.py                  # 🔧 Interface admin
│
├── 📁 issues/                    # 📱 APPLICATION "Projets"
│   ├── models.py                 # 📋 Modèles Project, Issue, Comment
│   ├── views.py                  # 🔧 API des projets/issues
│   ├── serializers.py            # 📤 Conversion JSON
│   └── admin.py                  # 🔧 Interface admin
│
└── manage.py                     # 🎛️ Gestionnaire Django
```

### 🤔 **Projet vs Application - Quelle différence ?**

**PROJET** (`softdesk_support`) :
- Container global
- Configuration générale
- URLs principales
- **Un seul par site web**

**APPLICATIONS** (`users`, `issues`) :
- Modules fonctionnels
- Logique métier spécifique
- **Plusieurs par projet**
- Réutilisables dans d'autres projets

## 🗄️ **Les Modèles Django (ORM)**

### **ORM = Object-Relational Mapping**

Django traduit automatiquement entre Python et SQL :

```python
# ✅ PYTHON (Django ORM)
user = User.objects.get(username='admin')
projects = Project.objects.filter(author=user)

# ⚡ SQL GÉNÉRÉ AUTOMATIQUEMENT
SELECT * FROM users_user WHERE username = 'admin';
SELECT * FROM issues_project WHERE author_id = 1;
```

### **Types de champs courants :**

```python
class Project(models.Model):
    # Texte
    name = models.CharField(max_length=200)           # VARCHAR(200)
    description = models.TextField()                  # TEXT
    
    # Choix multiples
    type = models.CharField(max_length=20, choices=PROJECT_TYPES)
    
    # Relations
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Clé étrangère
    contributors = models.ManyToManyField(User, through='Contributor')  # Many-to-Many
    
    # Dates
    created_time = models.DateTimeField(auto_now_add=True)  # Automatique à la création
    updated_time = models.DateTimeField(auto_now=True)     # Automatique à la modification
```

### **Relations expliquées :**

```python
# 🔗 OneToMany (ForeignKey)
class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Un projet → Un auteur
    # Un auteur → Plusieurs projets

# 🔗 ManyToMany
class Project(models.Model):
    contributors = models.ManyToManyField(User, through='Contributor')
    # Un projet → Plusieurs contributeurs
    # Un contributeur → Plusieurs projets

# 🔗 OneToOne
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Un profil → Un utilisateur uniquement
```

## 🔄 **Migrations Django**

### **Qu'est-ce qu'une migration ?**

Les migrations sont des fichiers Python qui décrivent les changements à apporter à la base de données.

```bash
# 1. Créer une migration après modification des modèles
poetry run python manage.py makemigrations

# 2. Appliquer les migrations à la base de données
poetry run python manage.py migrate
```

### **Exemple de migration générée :**

```python
# 0001_initial.py
class Migration(migrations.Migration):
    dependencies = []
    
    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
    ]
```

## 🛣️ **Système d'URLs Django**

### **Hiérarchie des URLs :**

```python
# 1. PROJET PRINCIPAL (softdesk_support/urls.py)
urlpatterns = [
    path('admin/', admin.site.urls),           # Interface admin
    path('api/', include(router.urls)),        # Délégation aux apps
]

# 2. ROUTEUR DRF (automatique)
router = DefaultRouter()
router.register(r'users', UserViewSet)        # /api/users/
router.register(r'projects', ProjectViewSet)  # /api/projects/
```

### **URL Patterns expliqués :**

```python
# Patterns basiques
path('users/', views.user_list),                    # /users/
path('users/<int:pk>/', views.user_detail),         # /users/123/
path('projects/<str:name>/', views.project_by_name) # /projects/mon-projet/

# Avec Django REST Framework
router.register(r'users', UserViewSet)
# Génère automatiquement :
# GET    /api/users/          → list()
# POST   /api/users/          → create()
# GET    /api/users/1/        → retrieve()
# PUT    /api/users/1/        → update()
# DELETE /api/users/1/        → destroy()
```

## ⚙️ **Settings Django**

### **Configuration centralisée :**

```python
# settings.py - Configuration de votre projet

# Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Applications installées
INSTALLED_APPS = [
    'django.contrib.admin',    # Interface admin
    'django.contrib.auth',     # Authentification
    'rest_framework',          # Django REST Framework
    'users',                   # Votre app users
    'issues',                  # Votre app issues
]

# Sécurité
SECRET_KEY = 'votre-clé-secrète'
DEBUG = True  # False en production !
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
```

## 🔐 **Système d'Authentification Django**

### **User model par défaut vs personnalisé :**

```python
# ❌ User Django par défaut
from django.contrib.auth.models import User
# Champs : username, email, password, first_name, last_name

# ✅ User personnalisé (votre projet)
class User(AbstractUser):
    age = models.PositiveIntegerField()
    can_be_contacted = models.BooleanField(default=True)
    can_data_be_shared = models.BooleanField(default=True)
```

### **Permissions et groupes :**

```python
# Vérifications dans les vues
if request.user.is_authenticated:
    # Utilisateur connecté
    
if request.user.has_perm('issues.add_project'):
    # Utilisateur a la permission de créer des projets
    
if request.user.groups.filter(name='Managers').exists():
    # Utilisateur dans le groupe "Managers"
```

## 🔧 **Admin Interface Django**

### **Interface d'administration automatique :**

```python
# admin.py
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'type', 'created_time']
    list_filter = ['type', 'created_time']
    search_fields = ['name', 'description']
    
    def get_queryset(self, request):
        # Optimisation N+1
        return super().get_queryset(request).select_related('author')
```

**Accès :** `http://127.0.0.1:8000/admin/`

## 🚀 **Commandes Django Essentielles**

```bash
# 🏗️ Création
poetry run python manage.py startproject monprojet     # Nouveau projet
poetry run python manage.py startapp monapp            # Nouvelle app

# 🗄️ Base de données
poetry run python manage.py makemigrations             # Créer migrations
poetry run python manage.py migrate                    # Appliquer migrations
poetry run python manage.py dbshell                    # Console SQL

# 👤 Utilisateurs
poetry run python manage.py createsuperuser           # Créer admin
poetry run python manage.py changepassword admin      # Changer mot de passe

# 🔍 Débogage
poetry run python manage.py check                     # Vérifier projet
poetry run python manage.py shell                     # Console Python/Django
poetry run python manage.py runserver                 # Démarrer serveur

# 📊 Données
poetry run python manage.py loaddata fixture.json    # Charger données
poetry run python manage.py dumpdata app.model       # Exporter données
```

## 🌟 **Django REST Framework (DRF)**

### **Extension de Django pour les APIs :**

```python
# Vue Django classique (HTML)
def user_list(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})

# Vue DRF (JSON)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # Génère automatiquement CRUD en JSON
```

### **Serializers = Traducteurs JSON :**

```python
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'type']
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Nom trop court")
        return value
```

## 🎯 **Pourquoi Django pour SoftDesk ?**

### ✅ **Avantages choisis :**

1. **🚀 Rapidité de développement**
   - Admin automatique
   - ORM intégré
   - Authentification prête

2. **🛡️ Sécurité par défaut**
   - Protection CSRF
   - Prévention injection SQL
   - Gestion des permissions

3. **📈 Scalabilité**
   - Architecture modulaire
   - Cache intégré
   - Optimisations ORM

4. **🌐 Écosystème riche**
   - Django REST Framework
   - Packages tiers nombreux
   - Communauté active

### 🎓 **Pour OpenClassrooms :**

Django démontre votre maîtrise de :
- **Architecture MVC/MVT**
- **ORM et bases de données**
- **APIs REST**
- **Sécurité web**
- **Bonnes pratiques Python**

## 🔗 **Ressources pour approfondir**

- **[Documentation officielle](https://docs.djangoproject.com/)**
- **[Django REST Framework](https://www.django-rest-framework.org/)**
- **[Django Girls Tutorial](https://tutorial.djangogirls.org/)**
- **[Real Python Django](https://realpython.com/tutorials/django/)**

---

**🎯 Django vous permet de créer des applications web robustes rapidement, avec une architecture claire et des bonnes pratiques intégrées !**
