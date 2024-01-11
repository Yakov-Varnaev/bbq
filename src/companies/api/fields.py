from rest_framework.serializers import CharField


class LowercaseCharField(CharField):
    """
    An enhancement over django-rest-framework's CharField to allow
    case-insensitive serialization and deserialization of text.
    """

    def to_internal_value(self, data: str) -> str:
        return super().to_internal_value(data).strip().lower()

    def to_representation(self, value: str) -> str:
        return super().to_representation(value).strip().lower()
