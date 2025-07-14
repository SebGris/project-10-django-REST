from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre seulement aux auteurs 
    de modifier leurs propres ressources
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture seulement pour l'auteur
        return obj.author == request.user


class IsContributorOrReadOnly(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet
    """
    
    def has_permission(self, request, view):
        # L'utilisateur doit être authentifié
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Pour les projets, vérifier que l'utilisateur est contributeur
        if hasattr(obj, 'contributors'):
            return obj.contributors.filter(user=request.user).exists()
        
        # Pour les autres objets, vérifier via le projet associé
        if hasattr(obj, 'project'):
            return obj.project.contributors.filter(user=request.user).exists()
        
        return False


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur 
    du projet associé à la ressource
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Récupérer le projet selon le type d'objet
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'issue'):
            project = obj.issue.project
        else:
            project = obj
        
        # Vérifier que l'utilisateur est contributeur du projet
        return project.contributors.filter(user=request.user).exists()
