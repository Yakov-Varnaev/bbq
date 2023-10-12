from rest_framework import serializers

from companies.api.serializers.defaults import CurrentPointDefault
from companies.models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentCreateSerialzier(DepartmentSerializer):
    point = serializers.HiddenField(default=CurrentPointDefault())

    def to_representation(self, instance: Department) -> dict:
        return DepartmentSerializer(instance).data
