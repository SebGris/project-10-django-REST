from rest_framework import permissions



class IsAuthor(permissions.BasePermission):
    """
    Seul l'auteur de la ressource peut modifier ou supprimer.
    Les autres utilisateurs ont un accès en lecture seule.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
