"""
Configuration commune pour tous les tests SoftDesk
"""
import os
import django

# Configuration Django (DOIT être fait AVANT d'importer les modèles)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_support.settings')
django.setup()

# Imports Django après setup
from users.models import User  # noqa: E402
from issues.models import Project, Contributor, Issue, Comment  # noqa: E402

# Variables de test communes
TEST_USER_DATA = {
    'author': {
        'username': 'test_author',
        'email': 'author@test.com',
        'password': 'TestPass123!',
        'age': 25
    },
    'contributor': {
        'username': 'test_contributor',
        'email': 'contributor@test.com',
        'password': 'TestPass123!',
        'age': 30
    },
    'commenter': {
        'username': 'test_commenter',
        'email': 'commenter@test.com',
        'password': 'TestPass123!',
        'age': 28
    }
}

def cleanup_test_data():
    """Nettoyer toutes les données de test"""
    # Nettoyer les utilisateurs de test
    test_usernames = [data['username'] for data in TEST_USER_DATA.values()]
    test_usernames.extend(['author_test', 'contributor_test', 'test_issue_author'])
    User.objects.filter(username__in=test_usernames).delete()
    
    # Nettoyer les projets de test
    test_project_names = ['Test Project', 'Test Project Issues', 'Test Nested Routes Project']
    Project.objects.filter(name__icontains='test').delete()

def create_test_users():
    """Créer les utilisateurs de test standards"""
    users = {}
    for role, data in TEST_USER_DATA.items():
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults=data
        )
        users[role] = user
    return users
