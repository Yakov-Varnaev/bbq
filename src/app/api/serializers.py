from rest_framework.serializers import Field


class CurrentCompanyDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> int:
        return serializer_field.context["request"]
