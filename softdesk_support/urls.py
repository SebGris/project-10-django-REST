"""
URL configuration for softdesk_support project.

Configuration avec routes imbriquées (nested routes) pour respecter l'architecture REST.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import des ViewSets
from users.views import UserViewSet
from issues.views import ProjectViewSet, ContributorViewSet, IssueViewSet, CommentViewSet


# Routeur principal
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')

# Routes imbriquées pour les projets
projects_router = routers.NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'contributors', ContributorViewSet, basename='project-contributors')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')

# Routes imbriquées pour les issues
issues_router = routers.NestedDefaultRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

# Routeur pour les issues globales (optionnel, pour accès direct)
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
    
    # Routes principales (users, projects, issues, comments - accès direct)
    path('api/', include(router.urls)),
    
    # Routes imbriquées (projects/{id}/contributors, projects/{id}/issues)
    path('api/', include(projects_router.urls)),
    
    # Routes imbriquées (projects/{id}/issues/{id}/comments)
    path('api/', include(issues_router.urls)),
]
