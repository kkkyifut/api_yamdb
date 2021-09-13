from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrSuperuserOnly(permissions.BasePermission):
    """Разрешение на доступ к ресурсу Users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == 'admin'


class IsModeratorOrAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение на доступ к ресурсам Review и Comment.
       Не накладывает ограничения на админа и суперпользователя."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or obj.author == request.user
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение на доступ к ресурсам Title, Category, Genre."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            )
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and (
                    request.user.is_superuser
                    or request.user.role == 'admin'
                )
            )
        )
