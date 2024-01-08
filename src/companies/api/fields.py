from rest_framework.serializers import CharField


class LowercaseCharField(CharField):
    """
    An enhancement over django-rest-framework's CharField to allow
    case-insensitive serialization and deserialization of text.
    """

    def to_internal_value(self, data: str) -> str:
        value: str = super().to_internal_value(data)
        return value.lower()

    def to_representation(self, value: str) -> str:
        data: str = super().to_representation(value)
        return data.lower()
