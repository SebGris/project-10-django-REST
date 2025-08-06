from rest_framework import permissions


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