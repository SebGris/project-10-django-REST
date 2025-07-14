from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorViewSet

# Créer le routeur pour les ViewSets
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'contributors', ContributorViewSet, basename='contributor')

# Définir les patterns d'URL
urlpatterns = [
    path('', include(router.urls)),
]
