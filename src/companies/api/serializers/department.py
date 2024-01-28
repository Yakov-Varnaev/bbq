from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from companies.api.fields import LowercaseCharField
from companies.api.serializers import CurrentDepartmentDefault, CurrentPointDefault
from companies.models import Category, Department, Procedure


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class DepartmentCreateSerialzier(DepartmentSerializer):
    point = serializers.HiddenField(default=CurrentPointDefault())

    def to_representation(self, instance: Department) -> dict:
        return DepartmentSerializer(instance).data


class CategorySerializer(serializers.ModelSerializer):
    name = LowercaseCharField()

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
        read_only_fields = ("id",)


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = (
            "id",
            "name",
            "category",
            "department",
        )
        read_only_fields = ("id",)


class ProcedureCreateUpdateSerialzier(ProcedureSerializer):
    department = serializers.HiddenField(default=CurrentDepartmentDefault())

    class Meta(ProcedureSerializer.Meta):
        validators = [
            UniqueTogetherValidator(
                queryset=Procedure.objects.all(),
                fields=["name", "department"],
            ),
        ]

    def to_representation(self, instance: Procedure) -> dict:
        return ProcedureSerializer(instance).data
