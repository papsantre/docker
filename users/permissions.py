from rest_framework import permissions


class IsUserOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем аккаунта"""

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
        return False


class IsModerator(permissions.BasePermission):
    """Проверяет, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="Moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
