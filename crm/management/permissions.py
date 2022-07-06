from rest_framework.permissions import BasePermission
from .models import Users


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
        if request.user.type == 'MANAGEMENT':
            return True
        return False
