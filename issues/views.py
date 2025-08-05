from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from softdesk_support.permissions import (
    IsProjectAuthorOrContributor,
    IsProjectContributor,
    IsAuthorOrProjectAuthorOrReadOnly
)

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer, ProjectListSerializer, ProjectCreateUpdateSerializer,
    IssueSerializer, IssueListSerializer, CommentSerializer, ContributorSerializer
)

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet pour les projets"""
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, IsProjectAuthorOrContributor]
    
    def get_queryset(self):
        """Retourne uniquement les projets où l'utilisateur est contributeur"""
        # Utiliser contributors__user au lieu de contributors directement
        return Project.objects.filter(
            contributors__user=self.request.user
            ).select_related('author').prefetch_related('contributors__user').distinct()
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'list':
            return ProjectListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        """Créer un projet avec l'utilisateur actuel comme auteur et contributeur"""
        project = serializer.save(author=self.request.user)
        # Ajouter automatiquement l'auteur comme contributeur s'il n'existe pas déjà
        Contributor.objects.get_or_create(
            user=self.request.user, 
            project=project
        )
    
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur au projet"""
        project = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
        
        if Contributor.objects.filter(user=user, project=project).exists():
            return Response({'error': 'Déjà contributeur'}, status=status.HTTP_400_BAD_REQUEST)
        
        Contributor.objects.create(user=user, project=project)
        return Response({'message': f'{user.username} ajouté comme contributeur'}, status=status.HTTP_201_CREATED)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet pour les contributeurs d'un projet"""
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]
    
    def get_queryset(self):
        """Retourne uniquement les contributeurs du projet spécifié"""
        project_id = self.kwargs.get('project_pk')
        
        # S'assurer que l'utilisateur est contributeur ou auteur du projet
        project = get_object_or_404(Project, pk=project_id)
        
        # Check permission explicitement pour la liste
        if not (project.author == self.request.user or 
                project.contributors.filter(user=self.request.user).exists()):
            # On retourne un queryset vide si l'utilisateur n'a pas accès
            # La permission doit ensuite bloquer l'accès
            return Contributor.objects.none()
            
        return Contributor.objects.filter(project_id=project_id)
    
    def perform_create(self, serializer):
        """Crée un contributeur lié au projet et à l'utilisateur spécifiés"""
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)
        
        # Vérifie que l'utilisateur actuel est l'auteur du projet
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs")
            
        user_id = self.request.data.get('user_id')
        user = get_object_or_404(User, pk=user_id)
        
        # Vérifie si le contributeur existe déjà
        if Contributor.objects.filter(project=project, user=user).exists():
            raise ValidationError("Cet utilisateur est déjà contributeur")
            
        serializer.save(project=project, user=user)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet pour les issues d'un projet"""
    permission_classes = [IsAuthenticated, IsProjectContributor, IsAuthorOrProjectAuthorOrReadOnly]
    
    def get_serializer_class(self):
        """Retourne le serializer approprié selon l'action"""
        if self.action == 'list':
            return IssueListSerializer
        return IssueSerializer
    
    def get_queryset(self):
        """Retourne les issues du projet spécifié dans l'URL"""
        project_id = self.kwargs.get('project_pk')
        # Optimisation Green Code : select_related pour réduire les requêtes
        return Issue.objects.filter(project_id=project_id).select_related(
            'author', 'project', 'assignee'
        ).prefetch_related('comments')
    
    def perform_create(self, serializer):
        """Créer une issue avec l'auteur et le projet depuis l'URL"""
        project_id = self.kwargs.get('project_pk')
        # Optimisation Green Code : select_related pour charger les contributeurs en une seule requête
        project = get_object_or_404(
            Project.objects.select_related('author').prefetch_related('contributors__user'),
            pk=project_id
        )
        
        # Vérification optimisée en utilisant les données préchargées
        if not (project.author == self.request.user or 
                project.contributors.filter(user=self.request.user).exists()):
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
            
        # Sauvegarde avec l'utilisateur actuel comme auteur
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les commentaires d'une issue"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsProjectContributor]
    
    def get_queryset(self):
        """Retourne les commentaires de l'issue spécifiée dans l'URL"""
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        # Optimisation Green Code : select_related pour éviter les requêtes supplémentaires
        return Comment.objects.filter(
            issue_id=issue_id, 
            issue__project_id=project_id
        ).select_related('author', 'issue__project__author')
    
    def perform_create(self, serializer):
        """Créer un commentaire avec l'auteur et l'issue depuis l'URL"""
        issue_id = self.kwargs.get('issue_pk')
        # Optimisation Green Code : select_related pour charger le projet en une seule requête
        issue = get_object_or_404(
            Issue.objects.select_related('project'),
            pk=issue_id
        )
        serializer.save(author=self.request.user, issue=issue)
    
    def update(self, request, *args, **kwargs):
        """Override update pour vérifier les permissions"""
        # Optimisation Green Code : récupération unique de l'objet
        comment = self.get_object()
        
        if comment.author != request.user:
            return Response(
                {"detail": "Seul l'auteur du commentaire peut le modifier."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Override partial_update pour vérifier les permissions"""
        # Optimisation Green Code : récupération unique de l'objet
        comment = self.get_object()
        
        if comment.author != request.user:
            return Response(
                {"detail": "Seul l'auteur du commentaire peut le modifier."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy pour permettre à l'auteur du projet de supprimer"""
        # Optimisation Green Code : select_related pour éviter les requêtes en cascade
        comment = self.get_object()
        
        if comment.author != request.user and comment.issue.project.author != request.user:
            return Response(
                {"detail": "Seul l'auteur du commentaire ou l'auteur du projet peut supprimer ce commentaire."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)