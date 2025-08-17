# tests/conftest.py
"""
Configuration des fixtures pour les tests pytest
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire racine au path Python
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Configurer Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "softdesk_support.settings")
django.setup()

# Maintenant on peut importer les modèles Django
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from issues.models import Project, Issue

User = get_user_model()


@pytest.fixture
def api_client():
    """Client API pour les tests"""
    return APIClient()


@pytest.fixture
def create_user(db):
    """Factory pour créer des utilisateurs"""

    def _create_user(**kwargs):
        defaults = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!",
            "age": 25,
            "can_be_contacted": False,
            "can_data_be_shared": False,
        }
        defaults.update(kwargs)
        password = defaults.pop("password")

        # Utiliser create_user qui gère correctement le password
        # et évite le problème avec full_clean()
        user = User.objects.create_user(
            username=defaults.pop("username"),
            email=defaults.pop("email"),
            password=password,
            **defaults,
        )
        return user

    return _create_user


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Client API authentifié avec JWT"""
    user = create_user()
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    api_client.user = user
    return api_client


@pytest.fixture
def create_project(create_user):
    """Factory pour créer des projets"""

    def _create_project(**kwargs):
        defaults = {
            "name": "Test Project",
            "description": "Test Description",
            "type": "back-end",
        }
        defaults.update(kwargs)
        if "author" not in defaults:
            defaults["author"] = create_user(username="projectauthor")
        return Project.objects.create(**defaults)

    return _create_project


@pytest.fixture
def create_issue(create_project, create_user):
    """Factory pour créer des issues"""

    def _create_issue(**kwargs):
        defaults = {
            "name": "Test Issue",
            "description": "Issue Description",
            "priority": "MEDIUM",
            "tag": "TASK",
            "status": "To Do",
        }
        defaults.update(kwargs)
        if "project" not in defaults:
            defaults["project"] = create_project()
        if "author" not in defaults:
            defaults["author"] = defaults["project"].author
        return Issue.objects.create(**defaults)

    return _create_issue
