from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserRegistrationSerializer, UserSummarySerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs
    - Création de compte (accessible à tous)
    - Consultation des profils par ID
    - Modification de son propre profil uniquement
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """Création ouverte à tous, le reste nécessite authentification"""
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        """Serializer spécifique selon l'action"""
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'list':
            return UserSummarySerializer
        return UserSerializer
    
    def get_queryset(self):
        """Tous les utilisateurs sont visibles"""
        if self.request.user.is_authenticated:
            return User.objects.all()
        return User.objects.none()
    
    def update(self, request, *args, **kwargs):
        """Un utilisateur ne peut modifier que son propre profil"""
        instance = self.get_object()
        if instance != request.user:
            return Response(
                {"detail": "Vous ne pouvez modifier que votre propre profil."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Un utilisateur ne peut supprimer que son propre compte"""
        instance = self.get_object()
        if instance != request.user:
            return Response(
                {"detail": "Vous ne pouvez supprimer que votre propre compte."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Créer un utilisateur et retourner la réponse avec les données créées
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Retourner la réponse avec le UserSerializer standard
        response_serializer = UserSerializer(user)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
