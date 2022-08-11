from rest_framework.permissions import BasePermission


class IsAuthorize(BasePermission):
    """
    Grant permission for management authenticated
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsManagerCrm(BasePermission):
    """
    Grant permission for management user
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False
