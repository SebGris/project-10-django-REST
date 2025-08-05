from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from softdesk_support.permissions import IsOwnerOrReadOnly
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
        """
        Permissions spécifiques selon l'action :
        - Création : accessible à tous
        - Lecture : authentification requise
        - Modification/Suppression : propriétaire uniquement
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
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
    
    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """Consulter ou modifier son propre profil"""
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)