from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project, Contributor, Issue, Comment, User
from .serializers import (
    ProjectSerializer, 
    ProjectCreateUpdateSerializer,
    ContributorSerializer, 
    IssueSerializer, 
    CommentSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner seulement les projets où l'utilisateur est contributeur"""
        user = self.request.user
        # Récupérer les projets où l'utilisateur est contributeur
        return Project.objects.filter(contributors__user=user).distinct()
    
    def get_serializer_class(self):
        """Utiliser un serializer différent pour la création/modification"""
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        """Créer un projet et ajouter l'auteur comme contributeur"""
        user = self.request.user
        project = serializer.save(author=user)
        
        # Ajouter l'auteur comme contributeur automatiquement
        Contributor.objects.create(user=user, project=project)
    
    def perform_update(self, serializer):
        """Vérifier que seul l'auteur peut modifier le projet"""
        project = self.get_object()
        if project.author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut modifier ce projet.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier que seul l'auteur peut supprimer le projet"""
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut supprimer ce projet.")
        instance.delete()
    
    @action(detail=True, methods=['post'], url_path='add-contributor')
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur au projet"""
        project = self.get_object()
        
        # Vérifier que l'utilisateur est l'auteur du projet
        if project.author != request.user:
            return Response(
                {"error": "Seul l'auteur peut ajouter des contributeurs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        username = request.data.get('username')
        if not username:
            return Response(
                {"error": "Le nom d'utilisateur est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_to_add = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier si l'utilisateur est déjà contributeur
        if Contributor.objects.filter(user=user_to_add, project=project).exists():
            return Response(
                {"error": "Cet utilisateur est déjà contributeur du projet"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ajouter le contributeur
        contributor = Contributor.objects.create(user=user_to_add, project=project)
        serializer = ContributorSerializer(contributor)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['delete'], url_path='remove-contributor/(?P<user_id>[^/.]+)')
    def remove_contributor(self, request, pk=None, user_id=None):
        """Supprimer un contributeur du projet"""
        project = self.get_object()
        
        # Vérifier que l'utilisateur est l'auteur du projet
        if project.author != request.user:
            return Response(
                {"error": "Seul l'auteur peut supprimer des contributeurs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Ne pas permettre de supprimer l'auteur
        user_to_remove = get_object_or_404(User, id=user_id)
        if user_to_remove == project.author:
            return Response(
                {"error": "L'auteur ne peut pas être supprimé du projet"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Supprimer le contributeur
        try:
            contributor = Contributor.objects.get(user=user_to_remove, project=project)
            contributor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Contributor.DoesNotExist:
            return Response(
                {"error": "Cet utilisateur n'est pas contributeur du projet"},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def contributors(self, request, pk=None):
        """Lister les contributeurs d'un projet"""
        project = self.get_object()
        contributors = project.contributors.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)


class ContributorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet en lecture seule pour les contributeurs
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner seulement les contributeurs des projets accessibles"""
        user = self.request.user
        return Contributor.objects.filter(
            project__contributors__user=user
        ).distinct()
