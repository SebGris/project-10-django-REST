"""
Tests pour l'authentification et la gestion des utilisateurs
"""
import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    """Tests pour l'authentification JWT"""
    
    def test_user_registration(self, api_client):
        """Test de l'inscription d'un utilisateur"""
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'age': 20,
            'can_be_contacted': True,
            'can_data_be_shared': False
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'id' in response.data
        assert response.data['username'] == 'newuser'
        assert response.data['email'] == 'new@example.com'
        assert 'password' not in response.data
        
        # Vérifier que l'utilisateur est bien créé en base
        assert User.objects.filter(username='newuser').exists()
    
    def test_user_registration_underage(self, api_client):
        """Test de rejet pour utilisateur mineur (moins de 15 ans)"""
        url = reverse('user-list')
        data = {
            'username': 'younguser',
            'email': 'young@example.com',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
            'age': 14,  # Trop jeune (< 15 ans)
            'can_be_contacted': False,
            'can_data_be_shared': False
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'age' in response.data
        assert User.objects.filter(username='younguser').exists() is False
    
    def test_user_registration_password_mismatch(self, api_client):
        """Test avec mots de passe qui ne correspondent pas"""
        url = reverse('user-list')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123!',
            'password_confirm': 'DifferentPass123!',
            'age': 25,
            'can_be_contacted': False,
            'can_data_be_shared': False
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data or 'password_confirm' in response.data
    
    def test_jwt_token_obtain(self, api_client, create_user):
        """Test d'obtention du token JWT"""
        # Créer un utilisateur avec un mot de passe connu
        _ = create_user(username='jwtuser', password='JWTPass123!')
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'jwtuser',
            'password': 'JWTPass123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
    
    def test_jwt_token_invalid_credentials(self, api_client, create_user):
        """Test avec des identifiants invalides"""
        _ = create_user(username='testuser', password='GoodPassword123!')
        
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'WrongPassword123!'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_jwt_token_refresh(self, api_client, create_user):
        """Test de rafraîchissement du token"""
        from rest_framework_simplejwt.tokens import RefreshToken
        
        user = create_user()
        refresh = RefreshToken.for_user(user)
        
        url = reverse('token_refresh')
        data = {'refresh': str(refresh)}
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_authenticated_request(self, authenticated_client):
        """Test d'une requête authentifiée"""
        url = reverse('user-list')
        response = authenticated_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_unauthenticated_request(self, api_client):
        """Test qu'une requête non authentifiée est rejetée"""
        url = reverse('project-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED