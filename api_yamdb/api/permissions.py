from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


# Для доступа к ресурсу Users
class IsAdminOrSuperuserOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated
                and (request.user.is_superuser or request.user.role == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.user.is_authenticated
                and (request.user.is_superuser or request.user.role == 'admin')
        )


# Для доступа к ресурсам Review и Comment
# этот пермишен не накладывает ограничения на права админа и суперюзера,
class IsModeratorOrAuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS
                or (
                        request.user.is_authenticated
                        and (
                                request.user.is_superuser
                                or request.user.role == 'admin'
                                or request.user.role == 'moderator'
                                or obj.author == request.user
                        )
                )
        )
