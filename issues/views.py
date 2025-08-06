from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from softdesk_support.permissions import (
    IsProjectAuthorOrContributor,
    IsProjectContributor,
    IsAuthorOrProjectAuthorOrReadOnly
)

from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer, ProjectListSerializer, ProjectCreateUpdateSerializer,
    IssueSerializer, IssueListSerializer, CommentSerializer, ContributorSerializer,
    AddContributorSerializer
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
        
        # Utiliser le serializer pour valider les données
        serializer = AddContributorSerializer(
            data=request.data,
            context={'project': project, 'request': request}
        )
        
        if serializer.is_valid():
            contributor = serializer.save()
            # Retourner les données du contributeur créé
            contributor_serializer = ContributorSerializer(contributor)
            return Response(
                {
                    'message': f'{contributor.user.username} ajouté comme contributeur',
                    'contributor': contributor_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContributorViewSet(viewsets.ModelViewSet):
    """ViewSet pour les contributeurs d'un projet"""
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]  # Retirer IsProjectContributor pour éviter le paradoxe
    
    def get_queryset(self):
        """Retourne uniquement les contributeurs du projet spécifié"""
        project_id = self.kwargs.get('project_pk')
        
        # Optimisation : utiliser select_related pour éviter les requêtes supplémentaires
        try:
            project = Project.objects.select_related('author').prefetch_related('contributors__user').get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound("Projet non trouvé")
        
        # Vérification des permissions pour la lecture
        if not (project.author == self.request.user or 
                project.contributors.filter(user=self.request.user).exists()):
            raise PermissionDenied("Vous n'avez pas accès à ce projet")
            
        return Contributor.objects.filter(project=project).select_related('user')
    
    @transaction.atomic
    def perform_create(self, serializer):
        """Crée un contributeur lié au projet et à l'utilisateur spécifiés"""
        project_id = self.kwargs.get('project_pk')
        project = get_object_or_404(Project, pk=project_id)
        
        # Vérifie que l'utilisateur actuel est l'auteur du projet
        if project.author != self.request.user:
            raise PermissionDenied("Seul l'auteur du projet peut ajouter des contributeurs")
        
        # Le serializer ContributorSerializer gère déjà la validation
        serializer.save(project=project)


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
        # Correction: utiliser 'assigned_to' au lieu de 'assignee'
        return Issue.objects.filter(project_id=project_id).select_related(
            'author', 'project', 'assigned_to'
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
        
        # Valider l'assignee si fourni (utiliser assigned_to au lieu d'assignee)
        assigned_to_id = self.request.data.get('assigned_to')
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                # Vérifier que l'assigned_to est contributeur du projet
                if not project.contributors.filter(user=assigned_user).exists():
                    raise ValidationError("L'utilisateur assigné doit être un contributeur du projet")
            except User.DoesNotExist:
                raise ValidationError("L'utilisateur assigné n'existe pas")
            
        # Sauvegarde avec l'utilisateur actuel comme auteur
        serializer.save(author=self.request.user, project=project)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet pour les commentaires d'une issue"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne les commentaires de l'issue spécifiée dans l'URL"""
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        # Vérifier que l'utilisateur a accès au projet
        project = get_object_or_404(Project, pk=project_id)
        if not (project.author == self.request.user or 
                project.contributors.filter(user=self.request.user).exists()):
            raise PermissionDenied("Vous n'avez pas accès à ce projet")
        
        return Comment.objects.filter(
            issue_id=issue_id, 
            issue__project_id=project_id
        ).select_related('author', 'issue__project__author')
    
    def perform_create(self, serializer):
        """Créer un commentaire avec l'auteur et l'issue depuis l'URL"""
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        # Vérifier la cohérence entre issue et project
        issue = get_object_or_404(
            Issue.objects.select_related('project').prefetch_related('project__contributors__user'),
            pk=issue_id,
            project_id=project_id
        )
        
        # Vérifier que l'utilisateur est contributeur du projet
        project = issue.project
        if not (project.author == self.request.user or 
                project.contributors.filter(user=self.request.user).exists()):
            raise PermissionDenied("Vous devez être contributeur du projet pour commenter")
        
        serializer.save(author=self.request.user, issue=issue)
    
    def check_comment_permission(self, comment, for_deletion=False):
        """Méthode utilitaire pour vérifier les permissions sur un commentaire"""
        if for_deletion:
            if comment.author != self.request.user and comment.issue.project.author != self.request.user:
                raise PermissionDenied("Seul l'auteur du commentaire ou l'auteur du projet peut supprimer ce commentaire.")
        else:
            if comment.author != self.request.user:
                raise PermissionDenied("Seul l'auteur du commentaire peut le modifier.")
    
    def update(self, request, *args, **kwargs):
        """Override update pour vérifier les permissions"""
        comment = self.get_object()
        self.check_comment_permission(comment)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Override partial_update pour vérifier les permissions"""
        comment = self.get_object()
        self.check_comment_permission(comment)
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy pour permettre à l'auteur du projet de supprimer"""
        comment = self.get_object()
        self.check_comment_permission(comment, for_deletion=True)
        return super().destroy(request, *args, **kwargs)