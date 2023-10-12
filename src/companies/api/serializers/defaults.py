from rest_framework.serializers import Field

from django.shortcuts import get_object_or_404

from companies.models import Point


class CurrentPointDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Point:
        view_kwargs = serializer_field.context["view"].kwargs
        return get_object_or_404(Point, id=view_kwargs["point_pk"], company_id=view_kwargs["company_pk"])
