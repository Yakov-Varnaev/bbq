from rest_framework.serializers import CharField


class LowercaseCharField(CharField):
    """
    An enhancement over django-rest-framework's CharField to allow
    case-insensitive serialization and deserialization of text.
    """

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return data.lower()

    def to_representation(self, value):
        value = super().to_representation(value)
        return value.lower()
