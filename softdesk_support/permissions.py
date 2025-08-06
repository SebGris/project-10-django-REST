from rest_framework import permissions
from issues.models import Project


class IsProjectAuthorOrContributor(permissions.BasePermission):
    """
    Permission personnalisée pour les projets.
    - GET: Seuls les contributeurs peuvent voir le projet
    - PUT/PATCH/DELETE: Seul l'auteur peut modifier/supprimer le projet
    - POST (add_contributor): Seul l'auteur peut gérer les contributeurs
    """
    
    def has_object_permission(self, request, view, obj):
        # Vérifie que l'utilisateur fait partie des contributeurs du projet (relation contributors__user)
        if not obj.contributors.filter(user=request.user).exists():
            return False
            
        # Pour les actions de modification, suppression et ajout de contributeurs
        if view.action in ['update', 'partial_update', 'destroy', 'add_contributor']:
            return obj.author == request.user
            
        # Pour la lecture (tous les contributeurs)
        return True


class IsProjectContributorOrObjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet (ou auteur),
    et appliquer des règles fines sur les objets (issues, commentaires).
    - GET/POST : Tous les contributeurs du projet peuvent lire/créer
    - PUT/PATCH/DELETE : Seulement l'auteur de l'objet ou l'auteur du projet
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

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
        # On suppose que tous les objets ont un attribut project (direct ou via @property)
        project = obj.project
        if not project:
            return False

        # Vérifier que l'utilisateur est contributeur ou auteur du projet
        if not (project.author == request.user or project.contributors.filter(user=request.user).exists()):
            return False

        # Lecture/création pour tous les contributeurs
        if request.method in permissions.SAFE_METHODS or request.method == 'POST':
            return True

        # Modification : auteur de l'objet ou auteur du projet
        is_author = obj.author == request.user
        is_project_author = project.author == request.user
        return is_author or is_project_author


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission pour les profils utilisateur.
    - GET: Tous les utilisateurs authentifiés peuvent voir
    - PUT/PATCH/DELETE: Seulement le propriétaire du profil
    """
    
    def has_object_permission(self, request, view, obj):
        # Pour la modification, seulement le propriétaire
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj == request.user
        
        # Pour la lecture, tous les utilisateurs authentifiés
        return request.user.is_authenticated