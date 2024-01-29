from rest_framework.serializers import Field

from django.shortcuts import get_object_or_404

from companies.models import Company, Department, Employee, Point
from companies.models.stock import Stock


class CurrentCompanyDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Company:
        company_id = serializer_field.context["view"].kwargs["company_pk"]
        return Company.objects.get(id=company_id)


class CurrentPointDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Point:
        view_kwargs = serializer_field.context["view"].kwargs
        return get_object_or_404(Point, id=view_kwargs["point_pk"], company_id=view_kwargs["company_pk"])


class CurrentDepartmentDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Department:
        view_kwargs = serializer_field.context["view"].kwargs
        return get_object_or_404(
            Department,
            id=view_kwargs["department_pk"],
            point_id=view_kwargs["point_pk"],
            point__company_id=view_kwargs["company_pk"],
        )


class CurrentStockDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Stock:
        view_kwargs = serializer_field.context["view"].kwargs
        return get_object_or_404(
            Stock,
            id=view_kwargs["stock_pk"],
            point_id=view_kwargs["point_pk"],
            point__company_id=view_kwargs["company_pk"],
        )


class CurrentEmployeeDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Employee:
        view_kwargs = serializer_field.context["view"].kwargs
        return get_object_or_404(
            Employee,
            id=view_kwargs["employee_pk"],
            departments__point_id=view_kwargs["point_pk"],
            departments__point__company_id=view_kwargs["company_pk"],
        )
