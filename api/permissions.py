from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        is_admin = request.user.role == 'admin'
        return bool(request.user and (request.user.is_staff or is_admin))


class IsAdminOrUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False
        return obj.author == request.user or request.user.role in ['moderator', 'admin']


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
