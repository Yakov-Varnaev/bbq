from rest_framework.serializers import Field

from companies.models import Company


class CurrentCompanyDefault:
    requires_context = True

    def __call__(self, serializer_field: Field) -> Company:
        company_id = serializer_field.context["view"].kwargs["company_pk"]
        return Company.objects.get(id=company_id)
