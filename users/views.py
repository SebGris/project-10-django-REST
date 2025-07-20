from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserPublicSerializer, UserRegistrationSerializer, UserProfileSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des utilisateurs
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['list']:
            return UserPublicSerializer
        elif self.action == 'retrieve':
            # Les admins peuvent voir le profil complet, les autres voient la vue publique
            if self.request.user.is_superuser:
                return UserSerializer
            return UserPublicSerializer
        elif self.action in ['update', 'partial_update']:
            return UserProfileSerializer
        return UserSerializer
    
    def get_permissions(self):
        """
        Instantie et retourne la liste des permissions requises pour cette vue.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Optionnellement restreint les utilisateurs retournés
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            # Un utilisateur ne peut modifier que son propre profil
            # Sauf si c'est un superuser qui peut modifier tous les profils
            if self.request.user.is_superuser:
                return User.objects.all()
            return User.objects.filter(pk=self.request.user.pk)
        return User.objects.all()
    
    @action(detail=False, methods=['get', 'put', 'patch'])
    def profile(self, request):
        """
        Endpoint pour gérer le profil de l'utilisateur connecté
        """
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = UserProfileSerializer(request.user, data=request.data, partial=partial)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
