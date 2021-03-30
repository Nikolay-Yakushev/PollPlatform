from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser


class ActionsAdminPermission(IsAdminUser):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        raise PermissionDenied()