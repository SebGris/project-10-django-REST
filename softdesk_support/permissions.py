from rest_framework import permissions


class IsProjectAuthorOrContributor(permissions.BasePermission):
    """
    Permission personnalisée pour les projets.
    - Seuls les contributeurs peuvent voir le projet
    - Seul l'auteur peut modifier/supprimer le projet
    - Seul l'auteur peut gérer les contributeurs
    """
    
    def has_permission(self, request, view):
        # Pour la création, tout utilisateur authentifié peut créer
        if view.action == 'create':
            return request.user.is_authenticated
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # IMPORTANT: Seuls les contributeurs peuvent accéder au projet
        # Vérifier via la relation contributors__user
        if not obj.contributors.filter(user=request.user).exists():
            return False
            
        # Pour les actions de modification/suppression et gestion des contributeurs
        if view.action in ['update', 'partial_update', 'destroy', 'add_contributor', 'remove_contributor']:
            return obj.author == request.user
            
        # Pour la lecture (tous les contributeurs)
        return True


class IsProjectContributor(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet.
    Utilisée pour les Issues et Comments.
    Seuls les contributeurs peuvent accéder aux ressources du projet.
    """
    
    def has_permission(self, request, view):
        # Import local pour éviter les imports circulaires
        from issues.models import Project
        
        # Récupère le projet depuis l'URL (pour les nested routes)
        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False
            
        # Récupérer le projet ou retourner False s'il n'existe pas
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return False
            
        # L'auteur du projet a toujours accès
        if project.author == request.user:
            return True
        
        # Sinon, vérifier si l'utilisateur est dans la liste des contributeurs
        return project.contributors.filter(user=request.user).exists()
    
    def has_object_permission(self, request, view, obj):
        # Pour les commentaires, on veut permettre la lecture à tous les contributeurs
        # mais seulement l'auteur ou l'auteur du projet peut modifier
        project = getattr(obj, 'project', None)
        if not project and hasattr(obj, 'issue'):
            project = obj.issue.project
            
        if project:
            # Vérifier si l'utilisateur est contributeur ou auteur du projet
            if project.author == request.user:
                return True
            return project.contributors.filter(user=request.user).exists()
        return False


class IsAuthorOrProjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour les Issues et Comments.
    - Seuls les contributeurs peuvent accéder (lecture/écriture)
    - Auteur de l'objet peut modifier/supprimer
    - Auteur du projet peut tout faire
    """
    
    def has_permission(self, request, view):
        # Utilise IsProjectContributor pour vérifier l'accès de base
        return IsProjectContributor().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        # D'abord vérifier que l'utilisateur est contributeur
        project = getattr(obj, 'project', None)
        if not project:
            # Si on a une issue, le projet est directement accessible
            if hasattr(obj, 'issue') and obj.issue:
                project = obj.issue.project
            else:
                return False
                
        if not (project.author == request.user or 
                project.contributors.filter(user=request.user).exists()):
            return False
        
        # Lecture pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Modification/suppression : auteur de l'objet ou auteur du projet
        is_author = obj.author == request.user
        is_project_author = project.author == request.user
        
        return is_author or is_project_author


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission pour les profils utilisateur.
    - L'utilisateur peut voir et modifier uniquement son propre profil
    - Les autres peuvent voir certaines informations (selon RGPD)
    """
    
    def has_object_permission(self, request, view, obj):
        # Pour la modification, seulement le propriétaire
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj == request.user
        
        # Pour la lecture, tous les utilisateurs authentifiés
        return request.user.is_authenticated