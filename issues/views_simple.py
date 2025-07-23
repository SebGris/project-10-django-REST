"""
ViewSets simplifiés pour un projet OpenClassrooms
Version plus lisible et pédagogique
"""
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Project, Contributor, Issue, Comment, User
from .serializers import (
    ProjectSerializer, 
    ProjectCreateUpdateSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer
)
from .permissions_simple import (
    IsProjectAuthor,
    IsAuthorOrReadOnly,
    IsIssueAuthorOrProjectAuthor,
    IsCommentAuthorOrProjectAuthor
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets
    CRUD complet : Create, Read, Update, Delete
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthor]
    
    def get_queryset(self):
        """Retourner seulement les projets où l'utilisateur est contributeur ou auteur"""
        user = self.request.user
        return Project.objects.filter(
            models.Q(contributors__user=user) | models.Q(author=user)
        ).select_related('author').prefetch_related('contributors__user').distinct()
    
    def get_serializer_class(self):
        """Utiliser un serializer différent pour la création/modification"""
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        """Définir l'auteur lors de la création"""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='add-contributor')
    def add_contributor(self, request, pk=None):
        """Action personnalisée : Ajouter un contributeur au projet"""
        project = self.get_object()
        
        # Récupérer l'utilisateur à ajouter
        username = request.data.get('username')
        user_id = request.data.get('user_id')
        
        if not username and not user_id:
            return Response(
                {"error": "username ou user_id requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_to_add = User.objects.get(username=username) if username else User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        
        # Vérifier si déjà contributeur
        if project.is_user_contributor(user_to_add):
            return Response(
                {"error": "Utilisateur déjà contributeur"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Créer le contributeur
        contributor = Contributor.objects.create(user=user_to_add, project=project)
        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def contributors(self, request, pk=None):
        """Action personnalisée : Lister les contributeurs"""
        project = self.get_object()
        contributors = project.contributors.all()
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)


class ContributorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet pour les contributeurs - Lecture seule
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner les contributeurs accessibles à l'utilisateur"""
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée : /projects/{id}/contributors/
            try:
                project = Project.objects.get(id=project_id)
                if project.is_user_contributor(user):
                    return project.contributors.select_related('user').all()
                return Contributor.objects.none()
            except Project.DoesNotExist:
                return Contributor.objects.none()
        else:
            # Route directe : /contributors/
            return Contributor.objects.filter(
                project__contributors__user=user
            ).select_related('user', 'project').distinct()


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des issues
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsIssueAuthorOrProjectAuthor]
    
    def get_queryset(self):
        """Retourner les issues accessibles à l'utilisateur"""
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée : /projects/{id}/issues/
            try:
                project = Project.objects.get(id=project_id)
                if project.is_user_contributor(user):
                    return project.issues.select_related('author', 'assigned_to', 'project').all()
                return Issue.objects.none()
            except Project.DoesNotExist:
                return Issue.objects.none()
        else:
            # Route directe : /issues/
            return Issue.objects.filter(
                models.Q(project__contributors__user=user) | models.Q(project__author=user)
            ).select_related('author', 'assigned_to', 'project').distinct()
    
    def perform_create(self, serializer):
        """Définir l'auteur et le projet lors de la création"""
        user = self.request.user
        project_id = self.kwargs.get('project_pk') or self.request.data.get('project')
        
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise PermissionDenied("Projet non trouvé")
        
        # Vérifier que l'utilisateur est contributeur
        if not project.is_user_contributor(user):
            raise PermissionDenied("Vous devez être contributeur du projet")
        
        serializer.save(author=user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des commentaires
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentAuthorOrProjectAuthor]
    
    def get_queryset(self):
        """Retourner les commentaires accessibles à l'utilisateur"""
        user = self.request.user
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        if issue_id and project_id:
            # Route imbriquée : /projects/{id}/issues/{id}/comments/
            try:
                project = Project.objects.get(id=project_id)
                issue = Issue.objects.get(id=issue_id, project=project)
                
                if project.is_user_contributor(user):
                    return issue.comments.select_related('author', 'issue__project').all()
                return Comment.objects.none()
            except (Project.DoesNotExist, Issue.DoesNotExist):
                return Comment.objects.none()
        else:
            # Route directe : /comments/
            return Comment.objects.filter(
                models.Q(issue__project__contributors__user=user) | 
                models.Q(issue__project__author=user)
            ).select_related('author', 'issue__project').distinct()
    
    def perform_create(self, serializer):
        """Définir l'auteur et l'issue lors de la création"""
        user = self.request.user
        issue_id = self.kwargs.get('issue_pk') or self.request.data.get('issue')
        
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise PermissionDenied("Issue non trouvée")
        
        # Vérifier que l'utilisateur est contributeur du projet
        if not issue.project.is_user_contributor(user):
            raise PermissionDenied("Vous devez être contributeur du projet")
        
        serializer.save(author=user, issue=issue)
