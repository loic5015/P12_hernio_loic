from rest_framework.permissions import BasePermission


class IsSaler(BasePermission):
    """
    Grant permission for user saler
    """
    def has_permission(self, request, view):
        if request.user.groups.filter(name='saler').exists():
            return True
        return False


class IsSupport(BasePermission):
    """
    Grant permission for user support
    """

    def has_permission(self, request, view):
        if request.user.groups.filter(name='support').exists():
            return True
        return False