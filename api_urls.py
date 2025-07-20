from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from issues.views import ProjectViewSet, ContributorViewSet
from users.views import UserViewSet

@api_view(['GET'])
def api_root(request, format=None):
    """
    Point d'entrée principal de l'API SoftDesk
    """
    return Response({
        'authentication': {
            'token': reverse('token_obtain_pair', request=request, format=format),
            'refresh': reverse('token_refresh', request=request, format=format),
        },
        'endpoints': {
            'users': reverse('user-list', request=request, format=format),
            'projects': reverse('project-list', request=request, format=format),
            'contributors': reverse('contributor-list', request=request, format=format),
        }
    })

# Créer le routeur principal pour tous les ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet, basename='contributor')

# Définir les patterns d'URL
urlpatterns = [
    # Page d'accueil de l'API
    path('', api_root),
    # Endpoints d'authentification JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Tous les ViewSets (users, projects, contributors)
    path('', include(router.urls)),
]
