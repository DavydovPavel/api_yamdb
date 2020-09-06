from rest_framework import permissions


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_anonymous:
            return False
        is_admin = user.role == 'admin' or user.is_staff
        return bool(user and is_admin)


class IsAdminOrUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_anonymous:
            if request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False
        return obj.author == user or user.role in ['moderator', 'admin']


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
