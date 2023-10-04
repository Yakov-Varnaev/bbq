from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView


class IsCompanyOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            return False
        company_id = view.kwargs.get("company_id")
        return request.user.companies.filter(id=company_id).exists()
