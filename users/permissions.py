from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission pour les profils utilisateur.
    - GET: Tous les utilisateurs authentifiés peuvent voir
    - PUT/PATCH/DELETE: Seulement le propriétaire du profil
    """

    def has_object_permission(self, request, view, obj):
        # Lecture : tous les utilisateurs authentifiés
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Modification/Suppression : seulement le propriétaire
        return obj == request.user
