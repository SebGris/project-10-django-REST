from django.db.models import Prefetch
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import transaction

from .permissions import (
    IsProjectAuthorOrContributor,
    IsProjectContributorOrObjectAuthorOrReadOnly
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
        return Project.objects.filter(
            contributors__user=self.request.user
        ).select_related('author').prefetch_related('contributors__user').distinct().order_by('id')  # Ajouter order_by

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer
    
    def create(self, request, *args, **kwargs):
        """Override create pour retourner le projet complet après création"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Récupérer l'instance créée avec toutes les relations préchargées
        project = (
            Project.objects
            .select_related('author')
            .prefetch_related('contributors__user')
            .get(pk=serializer.instance.pk)
        )
        
        # Utiliser ProjectSerializer pour la réponse avec toutes les données
        output_serializer = ProjectSerializer(project)
        
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @transaction.atomic
    def perform_create(self, serializer):
        """Création atomique du projet et du contributeur"""
        serializer.save(author=self.request.user)
        # Le contributeur est créé automatiquement dans Project.save()
    
    @transaction.atomic
    @action(detail=True, methods=['post'])
    def add_contributor(self, request, pk=None):
        """Ajout atomique d'un contributeur"""
        project = self.get_object()
        
        serializer = AddContributorSerializer(
            data=request.data,
            context={'project': project, 'request': request}
        )
        
        if serializer.is_valid():
            contributor = serializer.save()
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
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retourne uniquement les contributeurs du projet spécifié"""
        project_id = self.kwargs.get('project_pk')
        
        try:
            project = (
                Project.objects
                .select_related('author')
                .prefetch_related('contributors__user')
                .get(pk=project_id)
            )
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
            raise PermissionDenied(
                "Seul l'auteur du projet peut ajouter des contributeurs"
            )
        
        serializer.save(project=project)


class IssueViewSet(viewsets.ModelViewSet):
    """ViewSet pour les issues d'un projet"""
    permission_classes = [IsAuthenticated, IsProjectContributorOrObjectAuthorOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return IssueListSerializer
        return IssueSerializer
    
    def get_queryset(self):
        """Retourne les issues du projet spécifié dans l'URL"""
        project_id = self.kwargs.get('project_pk')
        return Issue.objects.filter(project_id=project_id).select_related(
            'author', 'project', 'assigned_to'
        ).prefetch_related('comments').order_by('id')  # Ajouter order_by
    
    @transaction.atomic
    def perform_create(self, serializer):
        """Création atomique avec vérifications optimisées"""
        project_id = self.kwargs.get('project_pk')
        
        # Une seule requête pour vérifier le projet et les permissions
        project = get_object_or_404(
            Project.objects.prefetch_related(
                Prefetch(
                    'contributors',
                    queryset=Contributor.objects.filter(user=self.request.user),
                    to_attr='user_contribution'
                )
            ),
            pk=project_id
        )
        
        # Vérification optimisée des permissions
        if not project.user_contribution and project.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet")
        
        # Validation de l'assignee si fourni
        assigned_to_id = self.request.data.get('assigned_to')
        if assigned_to_id:
            # Vérifier en une seule requête
            if not project.contributors.filter(user_id=assigned_to_id).exists():
                raise ValidationError(
                    "L'utilisateur assigné doit être un contributeur du projet"
                )
        
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
        ).select_related('author', 'issue__project__author').order_by('id')  # Ajouter order_by
    
    @transaction.atomic
    def perform_create(self, serializer):
        """Création atomique avec vérifications optimisées"""
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        # Une seule requête pour tout vérifier
        issue = get_object_or_404(
            Issue.objects.select_related('project').only(
                'id', 'project_id', 'project__author_id'
            ),
            pk=issue_id,
            project_id=project_id
        )
        
        # Vérification optimisée
        is_contributor = issue.project.contributors.filter(
            user=self.request.user
        ).exists() if issue.project.author_id != self.request.user.id else True
        
        if not is_contributor:
            raise PermissionDenied(
                "Vous devez être contributeur du projet pour commenter"
            )
        
        serializer.save(author=self.request.user, issue=issue)
    
    def check_comment_permission(self, comment, for_deletion=False):
        """Vérification optimisée des permissions"""
        if for_deletion:
            # Pour la suppression, on vérifie avec les données préchargées
            if (comment.author_id != self.request.user.id and 
                comment.issue.project.author_id != self.request.user.id):
                raise PermissionDenied(
                    "Seul l'auteur du commentaire ou du projet peut supprimer"
                )
        else:
            if comment.author_id != self.request.user.id:
                raise PermissionDenied("Seul l'auteur peut modifier ce commentaire")
    
    def update(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_comment_permission(comment)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_comment_permission(comment)
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_comment_permission(comment, for_deletion=True)
        return super().destroy(request, *args, **kwargs)