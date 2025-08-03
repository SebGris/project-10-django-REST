from rest_framework import permissions



class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission simple : l'auteur a tous les droits, les autres peuvent seulement lire
    """
    def has_object_permission(self, request, view, obj):
        # Lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture seulement pour l'auteur
        return obj.author == request.user
