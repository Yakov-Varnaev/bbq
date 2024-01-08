from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from companies.models import Company


class IsCompanyOwner(permissions.BasePermission):
    message = _("Only company owner can perform this action.")

    def has_permission(self, request: Request, view: APIView) -> bool:
        from companies.api.viewsets import CompanyViewSet

        if request.user.is_anonymous:
            return False

        # CompanyViewSet is the root of the, so we have to check for the pk
        company_id = view.kwargs.get("pk" if isinstance(view, CompanyViewSet) else "company_pk")
        assert company_id is not None
        company = get_object_or_404(Company, id=company_id)
        return company.owner == request.user


class IsCompanyOwnerOrReadOnly(IsCompanyOwner):
    message = _("Only company owner can perform this action.")

    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return super().has_permission(request, view)


class IsSuperUser(permissions.BasePermission):
    message = _("Only superusers can perform this action.")

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.user and request.user.is_superuser)


class CreateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(request.method in permissions.SAFE_METHODS or request.method == "POST")
