from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import models
from .models import Project, Contributor, Issue, Comment, User
from .serializers import (
    ProjectSerializer,
    ProjectListSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
)
from .permissions import IsAuthor


class ProjectViewSet(viewsets.ModelViewSet):
    """Gestion des projets"""
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    
    def get_serializer_class(self):
        """Utiliser un serializer simplifié pour la liste"""
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    def get_queryset(self):
        """Projets où l'utilisateur est contributeur"""
        user = self.request.user
        return Project.objects.filter(contributors__user=user)
    
    def perform_create(self, serializer):
        """L'utilisateur devient auteur du projet"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur par son ID (auteur seulement)"""
        project = self.get_object()
        
        if project.author != request.user:
            return Response({"error": "Seul l'auteur peut ajouter des contributeurs"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"error": "user_id requis"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_to_add = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, 
                          status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "user_id doit être un nombre entier"}, 
                          status=status.HTTP_400_BAD_REQUEST) # inutile car serializer
        if project.is_user_contributor(user_to_add):
                return Response({"error": "Déjà contributeur"}, 
                              status=status.HTTP_400_BAD_REQUEST)    
        Contributor.objects.create(user=user_to_add, project=project)
        return Response({"message": f"Contributeur {user_to_add.username} (ID: {user_id}) ajouté"}, 
                          status=status.HTTP_201_CREATED)


class IssueViewSet(viewsets.ModelViewSet):
    """Gestion des issues"""
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthor]
    
    def get_queryset(self):
        """Issues des projets accessibles"""
        user = self.request.user
        return Issue.objects.filter(project__contributors__user=user)
    
    def perform_create(self, serializer):
        """Créer une issue"""
        project_id = self.request.data.get('project')
        try:
            project = Project.objects.get(id=project_id)
            if not project.is_user_contributor(self.request.user):
                raise permissions.PermissionDenied("Vous devez être contributeur")
            serializer.save(author=self.request.user, project=project)
        except Project.DoesNotExist:
            raise permissions.PermissionDenied("Projet non trouvé")
    
class CommentViewSet(viewsets.ModelViewSet):
    """Gestion des commentaires"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthor]

    def get_queryset(self):
        """Commentaires des projets accessibles"""
        user = self.request.user
        return Comment.objects.filter(
            models.Q(issue__project__contributors__user=user) | 
            models.Q(issue__project__author=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Créer un commentaire"""
        issue_id = self.request.data.get('issue')
        try:
            issue = Issue.objects.get(id=issue_id)
            if not issue.project.is_user_contributor(self.request.user):
                raise permissions.PermissionDenied("Vous devez être contributeur")
            serializer.save(author=self.request.user, issue=issue)
        except Issue.DoesNotExist:
            raise permissions.PermissionDenied("Issue non trouvée")
    
class ContributorViewSet(viewsets.ModelViewSet):
    """Gestion des contributeurs d'un projet"""
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Contributeurs du projet spécifié"""
        project_id = self.kwargs.get('project_pk')
        return Contributor.objects.filter(project_id=project_id)
    
    def perform_create(self, serializer):
        """Ajouter un contributeur (auteur du projet seulement)"""
        project_id = self.kwargs.get('project_pk')
        project = Project.objects.get(id=project_id)
        
        if project.author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut ajouter des contributeurs")
        
        # user_id devrait venir du request.data
        user_id = self.request.data.get('user_id')
        if not user_id:
            raise permissions.PermissionDenied("user_id requis")
            
        try:
            user_to_add = User.objects.get(id=user_id)
            if project.is_user_contributor(user_to_add):
                raise permissions.PermissionDenied("Déjà contributeur")
            serializer.save(project=project, user=user_to_add)
        except User.DoesNotExist:
            raise permissions.PermissionDenied("Utilisateur non trouvé")