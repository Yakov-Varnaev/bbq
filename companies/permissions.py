from rest_framework.permissions import SAFE_METHODS, BasePermission

from companies.models import Company


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsCompanyPointOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.company.owner == request.user


class AllowedToEmploy(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return Company.objects.filter(pk=view.kwargs['company_pk'], owner=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return Company.objects.filter(pk=view.kwargs['company_pk'], owner=request.user).exists()
