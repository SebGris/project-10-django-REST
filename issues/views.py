from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Project, Contributor, Issue, Comment, User
from .serializers import (
    CommentSerializer,
    ContributorSerializer,
    IssueSerializer,
    ProjectSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    """Gestion des projets"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Projets où l'utilisateur est contributeur ou auteur"""
        user = self.request.user
        return Project.objects.filter(
            models.Q(contributors__user=user) | models.Q(author=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """L'utilisateur devient auteur du projet"""
        serializer.save(author=self.request.user)
    
    def perform_update(self, serializer):
        """Seul l'auteur peut modifier"""
        if self.get_object().author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut modifier le projet")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Seul l'auteur peut supprimer"""
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("Seul l'auteur peut supprimer le projet")
        instance.delete()
    
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur (auteur seulement)"""
        project = self.get_object()
        
        if project.author != request.user:
            return Response({"error": "Seul l'auteur peut ajouter des contributeurs"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        username = request.data.get('username')
        if not username:
            return Response({"error": "username requis"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_to_add = User.objects.get(username=username)
            if project.is_user_contributor(user_to_add):
                return Response({"error": "Déjà contributeur"}, 
                              status=status.HTTP_400_BAD_REQUEST)
            
            Contributor.objects.create(user=user_to_add, project=project)
            return Response({"message": "Contributeur ajouté"}, 
                          status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, 
                          status=status.HTTP_404_NOT_FOUND)


class IssueViewSet(viewsets.ModelViewSet):
    """Gestion des issues"""
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Issues des projets accessibles"""
        user = self.request.user
        return Issue.objects.filter(
            models.Q(project__contributors__user=user) | models.Q(project__author=user)
        ).distinct()
    
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
    
    def perform_update(self, serializer):
        """Seul l'auteur de l'issue ou du projet peut modifier"""
        issue = self.get_object()
        user = self.request.user
        if issue.author != user and issue.project.author != user:
            raise permissions.PermissionDenied("Non autorisé")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Seul l'auteur de l'issue ou du projet peut supprimer"""
        user = self.request.user
        if instance.author != user and instance.project.author != user:
            raise permissions.PermissionDenied("Non autorisé")
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """Gestion des commentaires"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
    
    def perform_update(self, serializer):
        """Seul l'auteur du commentaire ou du projet peut modifier"""
        comment = self.get_object()
        user = self.request.user
        if comment.author != user and comment.issue.project.author != user:
            raise permissions.PermissionDenied("Non autorisé")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Seul l'auteur du commentaire ou du projet peut supprimer"""
        user = self.request.user
        if instance.author != user and instance.issue.project.author != user:
            raise permissions.PermissionDenied("Non autorisé")
        instance.delete()

class ContributorViewSet(viewsets.ModelViewSet):
    """Gestion des contributeurs"""
    # Comme ModelViewSet étend GenericAPIView,
    # fournir au moins les attributs queryset et serializer_class.
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    
    