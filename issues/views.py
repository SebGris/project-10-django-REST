from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
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
from .permissions import (
    IsProjectAuthorOrReadOnly,
    IsIssueAuthorOrProjectAuthor,
    IsCommentAuthorOrProjectAuthor,
    IsProjectContributor,
    CanModifyAssignedUser,
    IsContributorViewAccess
)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsProjectAuthorOrReadOnly]
    
    def get_queryset(self):
        """Retourner seulement les projets où l'utilisateur est contributeur ou auteur"""
        user = self.request.user
        # GREEN CODE: Optimiser les requêtes avec select_related et prefetch_related
        # pour éviter les requêtes N+1
        return Project.objects.filter(
            models.Q(contributors__user=user) | models.Q(author=user)
        ).select_related('author').prefetch_related(
            'contributors__user'  # Précharger les utilisateurs des contributeurs
        ).distinct()
    
    def get_serializer_class(self):
        """Utiliser un serializer différent pour la création/modification"""
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateUpdateSerializer
        return ProjectSerializer
    
    def perform_create(self, serializer):
        """Créer un projet - l'auteur sera automatiquement ajouté comme contributeur"""
        user = self.request.user
        serializer.save(author=user)
        # L'auteur est automatiquement ajouté comme contributeur via Project.save()
    
    # ✅ perform_update et perform_destroy supprimées - gérées par IsProjectAuthorOrReadOnly
    
    @action(detail=True, methods=['post'], url_path='add-contributor')
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur au projet"""
        project = self.get_object()
        
        # ✅ Plus de vérification manuelle ! IsProjectAuthorOrReadOnly s'en charge via @action
        
        username = request.data.get('username')
        user_id = request.data.get('user_id')
        
        if not username and not user_id:
            return Response(
                {"error": "Le nom d'utilisateur ou l'ID utilisateur est requis"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if username:
                user_to_add = User.objects.get(username=username)
            else:
                user_to_add = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Utilisateur non trouvé"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier si l'utilisateur est déjà contributeur
        if project.is_user_contributor(user_to_add):
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
        
        # ✅ Plus de vérification manuelle ! IsProjectAuthorOrReadOnly s'en charge
        
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
    ViewSet pour les contributeurs - support des routes imbriquées
    Accessible via /api/projects/{project_id}/contributors/
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributorViewAccess]
    
    def get_queryset(self):
        """Retourner les contributeurs du projet spécifié dans l'URL"""
        # Récupérer l'ID du projet depuis l'URL imbriquée
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée: /projects/{project_id}/contributors/
            try:
                project = Project.objects.get(id=project_id)
                # ✅ Plus de vérification manuelle ! IsContributorViewAccess s'en charge
                # GREEN CODE: Précharger les utilisateurs pour éviter N+1
                return project.contributors.select_related('user').all()
            except Project.DoesNotExist:
                return Contributor.objects.none()
        else:
            # Route directe: /contributors/ (tous les contributeurs accessibles)
            user = self.request.user
            # GREEN CODE: Optimiser avec select_related pour éviter N+1
            return Contributor.objects.filter(
                project__contributors__user=user
            ).select_related('user', 'project').distinct()


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des issues (problèmes/tâches)
    Support des routes imbriquées: /api/projects/{project_id}/issues/
    """
    serializer_class = IssueSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        IsProjectContributor, 
        IsIssueAuthorOrProjectAuthor,
        CanModifyAssignedUser
    ]
    
    def get_queryset(self):
        """Retourner les issues selon le contexte (imbriqué ou global)"""
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée: /projects/{project_id}/issues/
            try:
                project = Project.objects.get(id=project_id)
                # ✅ Plus de vérification manuelle ! IsProjectContributor s'en charge
                # GREEN CODE: Précharger les relations pour éviter N+1
                return project.issues.select_related('author', 'assigned_to', 'project').all()
            except Project.DoesNotExist:
                return Issue.objects.none()
        else:
            # Route directe: /issues/ (toutes les issues accessibles)
            # GREEN CODE: Optimiser avec select_related pour éviter N+1
            return Issue.objects.filter(
                models.Q(project__contributors__user=user) | models.Q(project__author=user)
            ).select_related('author', 'assigned_to', 'project').distinct()
    
    def create(self, request, *args, **kwargs):
        """Créer une issue - gérer les routes imbriquées"""
        # Si on est dans une route imbriquée, ajouter le project_id aux données
        project_id = self.kwargs.get('project_pk')
        if project_id:
            # Route imbriquée: ajouter le project aux données avant validation
            request.data['project'] = project_id
        
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Créer une issue - support des routes imbriquées"""
        # ✅ Plus de vérifications de permissions ! Les permission classes s'en chargent
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée: le projet est défini par l'URL
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise permissions.PermissionDenied("Projet non trouvé.")
        else:
            # Route directe: le projet doit être fourni dans les données
            project_id = self.request.data.get('project')
            if not project_id:
                raise permissions.PermissionDenied("Le projet est requis.")
            
            try:
                project = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                raise permissions.PermissionDenied("Projet non trouvé.")
        
        # ✅ Plus de vérifications manuelles ! CanModifyAssignedUser s'en charge
        # Sauvegarder avec l'auteur et le projet
        serializer.save(author=user, project=project)
    
    # ✅ perform_update et perform_destroy supprimées - gérées par IsIssueAuthorOrProjectAuthor


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des commentaires
    Support des routes imbriquées: /api/projects/{project_id}/issues/{issue_id}/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated, 
        IsProjectContributor, 
        IsCommentAuthorOrProjectAuthor
    ]
    
    def get_queryset(self):
        """Retourner les commentaires selon le contexte (imbriqué ou global)"""
        user = self.request.user
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        if issue_id and project_id:
            # Route imbriquée: /projects/{project_id}/issues/{issue_id}/comments/
            try:
                project = Project.objects.get(id=project_id)
                issue = Issue.objects.get(id=issue_id, project=project)
                
                # ✅ Plus de vérification manuelle ! IsProjectContributor s'en charge
                
                # GREEN CODE: Précharger les relations pour éviter N+1
                return issue.comments.select_related('author', 'issue__project').all()
            except (Project.DoesNotExist, Issue.DoesNotExist):
                return Comment.objects.none()
        else:
            # Route directe: /comments/ (tous les commentaires accessibles)
            # GREEN CODE: Optimiser avec select_related pour éviter N+1
            return Comment.objects.filter(
                models.Q(issue__project__contributors__user=user) | 
                models.Q(issue__project__author=user)
            ).select_related('author', 'issue__project').distinct()
    
    def create(self, request, *args, **kwargs):
        """Créer un commentaire - gérer les routes imbriquées"""
        # Si on est dans une route imbriquée, ajouter l'issue_id aux données
        issue_id = self.kwargs.get('issue_pk')
        if issue_id:
            # Route imbriquée: ajouter l'issue aux données avant validation
            request.data['issue'] = issue_id
        
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Créer un commentaire - support des routes imbriquées"""
        # ✅ Plus de vérifications de permissions ! Les permission classes s'en chargent
        user = self.request.user
        issue_id = self.kwargs.get('issue_pk')
        project_id = self.kwargs.get('project_pk')
        
        if issue_id and project_id:
            # Route imbriquée: l'issue est définie par l'URL
            try:
                project = Project.objects.get(id=project_id)
                issue = Issue.objects.get(id=issue_id, project=project)
            except (Project.DoesNotExist, Issue.DoesNotExist):
                raise permissions.PermissionDenied("Issue ou projet non trouvé.")
        else:
            # Route directe: l'issue doit être fournie dans les données
            issue_id = self.request.data.get('issue')
            if not issue_id:
                raise permissions.PermissionDenied("L'issue est requise.")
                
            try:
                issue = Issue.objects.get(id=issue_id)
                project = issue.project
            except Issue.DoesNotExist:
                raise permissions.PermissionDenied("Issue non trouvée.")
        
        # ✅ Plus de vérifications manuelles ! IsProjectContributor s'en charge
        # Sauvegarder avec l'auteur et l'issue
        serializer.save(author=user, issue=issue)
    
    # ✅ perform_update et perform_destroy supprimées - gérées par IsCommentAuthorOrProjectAuthor
