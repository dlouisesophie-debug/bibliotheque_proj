from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Permission qui permet la lecture à tous,
    mais l'écriture uniquement aux administrateurs.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return request.user and request.user.is_staff


class IsOwnerOrAdmin(BasePermission):
    """
    Permission qui permet à l'utilisateur de voir/modifier ses propres objets,
    et aux admins de tout voir/modifier.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.utilisateur == request.user