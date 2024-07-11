from rest_framework import permissions


class IsStaffUSerReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff and request.method == 'GET':
            return True
        elif request.user.is_superuser:
            return True
        return False 