"""
Permissions simplifiées pour un projet OpenClassrooms
Version plus simple et pédagogique
"""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission simple : seul l'auteur peut modifier/supprimer.
    Lecture autorisée pour tous les utilisateurs authentifiés qui ont accès à l'objet.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée (sera filtrée par get_queryset())
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture seulement pour l'auteur
        return obj.author == request.user


class IsProjectAuthor(permissions.BasePermission):
    """
    Permission simple : seul l'auteur du projet peut modifier/supprimer.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée (sera filtrée par get_queryset())
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture seulement pour l'auteur du projet
        return obj.can_user_modify(request.user)


class IsIssueAuthorOrProjectAuthor(permissions.BasePermission):
    """
    Permission pour les issues : auteur de l'issue OU auteur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée (sera filtrée par get_queryset())
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture pour l'auteur de l'issue OU l'auteur du projet
        return obj.author == request.user or obj.project.author == request.user


class IsCommentAuthorOrProjectAuthor(permissions.BasePermission):
    """
    Permission pour les commentaires : auteur du commentaire OU auteur du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée (sera filtrée par get_queryset())
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture pour l'auteur du commentaire OU l'auteur du projet
        return obj.author == request.user or obj.issue.project.author == request.user
