"""
URL configuration for softdesk_support project.

Configuration simplifiée avec tous les endpoints dans un seul fichier.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import des ViewSets
from users.views import UserViewSet
from issues.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet


# Créer le routeur pour tous les ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet, basename='contributor')
router.register(r'issues', IssueViewSet, basename='issue')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    # Interface d'administration Django
    path('admin/', admin.site.urls),
    
    # Interface d'authentification DRF (login/logout web)
    path('api-auth/', include('rest_framework.urls')),
    
    # Endpoints d'authentification JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Tous les endpoints de l'API (users, projects, contributors, issues, comments)
    path('api/', include(router.urls)),
]
