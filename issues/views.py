from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
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
        # Récupérer les projets où l'utilisateur est contributeur OU auteur
        return Project.objects.filter(
            models.Q(contributors__user=user) | models.Q(author=user)
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


class IssueViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour la gestion des issues (problèmes/tâches)
    """
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner seulement les issues des projets où l'utilisateur est contributeur"""
        user = self.request.user
        return Issue.objects.filter(
            models.Q(project__contributors__user=user) | models.Q(project__author=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Créer une issue - vérifier que l'utilisateur peut créer dans ce projet"""
        project_id = self.request.data.get('project')
        if not project_id:
            raise permissions.PermissionDenied("Le projet est requis.")
            
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise permissions.PermissionDenied("Projet non trouvé.")
        
        # Vérifier que l'utilisateur est contributeur du projet
        if not project.is_user_contributor(self.request.user):
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
        
        serializer.save(author=self.request.user)
    
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
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Retourner seulement les commentaires des issues accessibles"""
        user = self.request.user
        return Comment.objects.filter(
            models.Q(issue__project__contributors__user=user) | 
            models.Q(issue__project__author=user)
        ).distinct()
    
    def perform_create(self, serializer):
        """Créer un commentaire - vérifier que l'utilisateur peut commenter"""
        issue_id = self.request.data.get('issue')
        if not issue_id:
            raise permissions.PermissionDenied("L'issue est requise.")
            
        try:
            issue = Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            raise permissions.PermissionDenied("Issue non trouvée.")
        
        # Vérifier que l'utilisateur est contributeur du projet
        if not issue.project.is_user_contributor(self.request.user):
            raise permissions.PermissionDenied("Vous devez être contributeur du projet pour commenter.")
        
        serializer.save(author=self.request.user)
    
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
