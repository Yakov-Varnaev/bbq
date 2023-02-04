from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user
