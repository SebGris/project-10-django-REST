from rest_framework import permissions


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour les projets : seul l'auteur peut modifier/supprimer.
    Lecture autorisée pour tous les contributeurs.
    """
    
    def has_object_permission(self, request, view, obj):
        # Vérifier que l'utilisateur est contributeur pour la lecture
        if request.method in permissions.SAFE_METHODS:
            return obj.is_user_contributor(request.user)
        
        # Permissions d'écriture seulement pour l'auteur du projet
        return obj.can_user_modify(request.user)


class IsIssueAuthorOrProjectAuthor(permissions.BasePermission):
    """
    Permission pour les issues : auteur de l'issue OU auteur du projet peut modifier/supprimer.
    Lecture autorisée pour tous les contributeurs du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Permissions de lecture pour tous les contributeurs du projet
        if request.method in permissions.SAFE_METHODS:
            return obj.project.is_user_contributor(user)
        
        # Permissions d'écriture pour l'auteur de l'issue OU l'auteur du projet
        return obj.author == user or obj.project.author == user


class IsCommentAuthorOrProjectAuthor(permissions.BasePermission):
    """
    Permission pour les commentaires : auteur du commentaire OU auteur du projet peut modifier/supprimer.
    Lecture autorisée pour tous les contributeurs du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Permissions de lecture pour tous les contributeurs du projet
        if request.method in permissions.SAFE_METHODS:
            return obj.issue.project.is_user_contributor(user)
        
        # Permissions d'écriture pour l'auteur du commentaire OU l'auteur du projet
        return obj.author == user or obj.issue.project.author == user


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet.
    Utilisée pour la création d'issues et commentaires.
    """
    
    def has_permission(self, request, view):
        # Pour les routes imbriquées, vérifier le projet parent
        project_id = view.kwargs.get('project_pk')
        if project_id:
            try:
                from .models import Project
                project = Project.objects.get(id=project_id)
                return project.is_user_contributor(request.user)
            except Project.DoesNotExist:
                return False
        
        # Pour les routes directes, la vérification se fera dans perform_create
        return True
    
    def has_object_permission(self, request, view, obj):
        # Vérifier que l'utilisateur est contributeur du projet associé
        if hasattr(obj, 'project'):
            return obj.project.is_user_contributor(request.user)
        elif hasattr(obj, 'issue'):
            return obj.issue.project.is_user_contributor(request.user)
        return False


class CanModifyAssignedUser(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur assigné est contributeur du projet.
    """
    
    def has_permission(self, request, view):
        assigned_to_id = request.data.get('assigned_to')
        if not assigned_to_id:
            return True  # Pas d'assignation, pas de problème
        
        # Récupérer le projet selon le contexte
        project_id = view.kwargs.get('project_pk') or request.data.get('project')
        if project_id:
            try:
                from .models import Project, User
                project = Project.objects.get(id=project_id)
                assigned_user = User.objects.get(id=assigned_to_id)
                return project.is_user_contributor(assigned_user)
            except (Project.DoesNotExist, User.DoesNotExist):
                return False
        
        return True


class IsContributorViewAccess(permissions.BasePermission):
    """
    Permission pour l'accès aux contributeurs : lecture seule pour les contributeurs du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        # Seule la lecture est autorisée pour les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return obj.project.is_user_contributor(request.user)
        return False
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        else:
            project = obj
        
        # Vérifier que l'utilisateur est contributeur du projet
        return project.contributors.filter(user=request.user).exists()
