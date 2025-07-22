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


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des projets
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
    
    def create(self, request, *args, **kwargs):
        """Créer un projet et retourner la réponse complète avec l'ID"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Retourner la réponse avec le ProjectSerializer complet (avec ID)
        instance = serializer.instance
        response_serializer = ProjectSerializer(instance, context={'request': request})
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_update(self, serializer):
        """Vérifier que seul l'auteur peut modifier le projet"""
        project = self.get_object()
        if not project.can_user_modify(self.request.user):
            raise permissions.PermissionDenied("Seul l'auteur peut modifier ce projet.")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier que seul l'auteur peut supprimer le projet"""
        if not instance.can_user_modify(self.request.user):
            raise permissions.PermissionDenied("Seul l'auteur peut supprimer ce projet.")
        instance.delete()
    
    @action(detail=True, methods=['post'], url_path='add-contributor')
    def add_contributor(self, request, pk=None):
        """Ajouter un contributeur au projet"""
        project = self.get_object()
        
        # Vérifier que l'utilisateur est l'auteur du projet
        if not project.can_user_modify(request.user):
            return Response(
                {"error": "Seul l'auteur peut ajouter des contributeurs"},
                status=status.HTTP_403_FORBIDDEN
            )
        
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
        
        # Vérifier que l'utilisateur est l'auteur du projet
        if not project.can_user_modify(request.user):
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
    ViewSet pour les contributeurs - support des routes imbriquées
    Accessible via /api/projects/{project_id}/contributors/
    """
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner les contributeurs du projet spécifié dans l'URL"""
        # Récupérer l'ID du projet depuis l'URL imbriquée
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée: /projects/{project_id}/contributors/
            try:
                project = Project.objects.get(id=project_id)
                # Vérifier que l'utilisateur peut accéder à ce projet
                if not project.is_user_contributor(self.request.user):
                    return Contributor.objects.none()
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
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner les issues selon le contexte (imbriqué ou global)"""
        user = self.request.user
        project_id = self.kwargs.get('project_pk')
        
        if project_id:
            # Route imbriquée: /projects/{project_id}/issues/
            try:
                project = Project.objects.get(id=project_id)
                # Vérifier que l'utilisateur peut accéder à ce projet
                if not project.is_user_contributor(user):
                    return Issue.objects.none()
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
        
        # Vérifier que l'utilisateur est contributeur du projet
        if not project.is_user_contributor(user):
            raise permissions.PermissionDenied("Vous devez être contributeur du projet pour créer une issue.")
        
        # Vérifier assigned_to si fourni
        assigned_to_id = self.request.data.get('assigned_to')
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                if not project.is_user_contributor(assigned_user):
                    raise permissions.PermissionDenied("L'utilisateur assigné doit être contributeur du projet.")
            except User.DoesNotExist:
                raise permissions.PermissionDenied("Utilisateur assigné non trouvé.")
        
        # Sauvegarder avec l'auteur et le projet
        serializer.save(author=user, project=project)
    
    def perform_update(self, serializer):
        """Vérifier que l'utilisateur peut modifier cette issue"""
        issue = self.get_object()
        user = self.request.user
        
        # Seul l'auteur de l'issue ou l'auteur du projet peut modifier
        if issue.author != user and issue.project.author != user:
            raise permissions.PermissionDenied("Seul l'auteur de l'issue ou l'auteur du projet peut la modifier.")
        
        # Vérifier assigned_to si fourni
        assigned_to_id = self.request.data.get('assigned_to')
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                if not issue.project.is_user_contributor(assigned_user):
                    raise permissions.PermissionDenied("L'utilisateur assigné doit être contributeur du projet.")
            except User.DoesNotExist:
                raise permissions.PermissionDenied("Utilisateur assigné non trouvé.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier que l'utilisateur peut supprimer cette issue"""
        user = self.request.user
        
        # Seul l'auteur de l'issue ou l'auteur du projet peut supprimer
        if instance.author != user and instance.project.author != user:
            raise permissions.PermissionDenied("Seul l'auteur de l'issue ou l'auteur du projet peut la supprimer.")
        
        instance.delete()


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des commentaires
    Support des routes imbriquées: /api/projects/{project_id}/issues/{issue_id}/comments/
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
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
                
                # Vérifier que l'utilisateur peut accéder à ce projet
                if not project.is_user_contributor(user):
                    return Comment.objects.none()
                
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
        
        # Vérifier que l'utilisateur est contributeur du projet
        if not project.is_user_contributor(user):
            raise permissions.PermissionDenied("Vous devez être contributeur du projet pour commenter.")
        
        # Sauvegarder avec l'auteur et l'issue
        serializer.save(author=user, issue=issue)
    
    def perform_update(self, serializer):
        """Vérifier que l'utilisateur peut modifier ce commentaire"""
        comment = self.get_object()
        user = self.request.user
        
        # Seul l'auteur du commentaire peut le modifier
        if comment.author != user:
            raise permissions.PermissionDenied("Seul l'auteur du commentaire peut le modifier.")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Vérifier que l'utilisateur peut supprimer ce commentaire"""
        user = self.request.user
        
        # Seul l'auteur du commentaire ou l'auteur du projet peut supprimer
        if instance.author != user and instance.issue.project.author != user:
            raise permissions.PermissionDenied("Seul l'auteur du commentaire ou l'auteur du projet peut le supprimer.")
        
        instance.delete()
