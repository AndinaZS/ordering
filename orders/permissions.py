from rest_framework import permissions


class IsVerified(permissions.BasePermission):
    # class for check verification user's email
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_verified
