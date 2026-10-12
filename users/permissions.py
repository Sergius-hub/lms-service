from rest_framework import permissions

class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        """Пользователь залогинен."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Доступ к одному объекту разрешен."""
        return obj.owner == request.user
