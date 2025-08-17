from rest_framework import permissions
from .models import Project


class IsProjectAuthorOrContributor(permissions.BasePermission):
    """
    Permission personnalisée pour les projets.
    - GET: Seuls les contributeurs peuvent voir le projet
    - PUT/PATCH/DELETE: Seul l'auteur peut modifier/supprimer le projet
    - POST (add_contributor): Seul l'auteur peut gérer les contributeurs
    """
    
    def has_object_permission(self, request, view, obj):
        # Optimisation : vérifier d'abord si c'est l'auteur (plus rapide)
        is_author = obj.author == request.user
        
        # Si c'est l'auteur, il a tous les droits
        if is_author:
            return True
        
        # Sinon, vérifier s'il est contributeur
        is_contributor = obj.contributors.filter(user=request.user).exists()
        
        # Si pas contributeur du tout, refuser
        if not is_contributor:
            return False
        
        # Pour les actions de modification, seul l'auteur
        if view.action in ['update', 'partial_update', 'destroy', 'add_contributor']:
            return False  # Déjà vérifié que ce n'est pas l'auteur
        
        # Pour la lecture, les contributeurs peuvent accéder
        return True


class IsProjectContributorOrObjectAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet (ou auteur),
    et appliquer des règles fines sur les objets (issues, commentaires).
    - GET/POST : Tous les contributeurs du projet peuvent lire/créer
    - PUT/PATCH/DELETE : Seulement l'auteur de l'objet ou l'auteur du projet
    """

    def has_permission(self, request, view):
        """Vérifie l'accès au niveau de la vue (liste/création)"""
        project_id = view.kwargs.get('project_pk')
        if not project_id:
            return False

        try:
            # Optimisation : ne charger que les champs nécessaires
            project = Project.objects.only('author_id').get(pk=project_id)
        except Project.DoesNotExist:
            return False

        # L'auteur du projet a toujours accès
        if project.author_id == request.user.id:
            return True

        # Sinon, vérifier si l'utilisateur est contributeur
        # Optimisation : utiliser exists() qui s'arrête dès qu'il trouve
        return project.contributors.filter(user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        """Vérifie l'accès au niveau de l'objet spécifique"""
        # Récupérer le projet associé
        project = getattr(obj, 'project', None)
        if not project:
            return False

        # Optimisation : vérifier d'abord si c'est l'auteur du projet
        is_project_author = project.author == request.user
        
        # L'auteur du projet a tous les droits
        if is_project_author:
            return True
        
        # Vérifier que l'utilisateur est contributeur
        is_contributor = project.contributors.filter(user=request.user).exists()
        if not is_contributor:
            return False

        # Lecture : tous les contributeurs
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Création : tous les contributeurs (POST n'arrive pas ici normalement)
        if request.method == 'POST':
            return True

        # Modification/Suppression : seulement l'auteur de l'objet
        return obj.author == request.user
