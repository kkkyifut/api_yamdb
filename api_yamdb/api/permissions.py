from rest_framework import permissions


class IsAdminOrSuperuserOnly(permissions.BasePermission):
    """Разрешение на доступ к ресурсу Users."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_superuser or request.user.is_admin)
        )


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
            or request.user.is_admin
            or request.user.is_moderator
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
                    or request.user.is_admin
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
                    or request.user.is_admin
                )
            )
        )
