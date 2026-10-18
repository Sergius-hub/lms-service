from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    """Проверка пользователя в группе moderators."""

    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверка поля Owner и запрос пользовтеля."""

    def has_permission(self, request, view):
        """Пользователь залогинен."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Доступ к одному объекту разрешен."""
        return obj.owner == request.user


class IsSelfOrAdmin(permissions.BasePermission):
    """Пользователь работает только со своим профилем. Админ — со всеми."""

    message = "Можно работать только со своим профилем."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_staff or user.is_superuser:
            return True
        return obj.pk == user.pk