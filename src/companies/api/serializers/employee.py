from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from django.utils.translation import gettext_lazy as _

from companies.api.serializers import CurrentEmployeeDefault, ProcedureSerializer
from companies.models import Employee, MasterProcedure


class EmployeeSerializer(serializers.ModelSerializer):
    def validate_departments(self, departments: list[int]) -> list[int]:
        if len(set(departments)) != len(departments):
            raise ValidationError(_("departments duplication"))
        return departments

    class Meta:
        model = Employee
        fields = "__all__"


class EmployeeShortSerialiser(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

    class Meta:
        model = Employee
        fields = (
            "id",
            "first_name",
            "last_name",
        )


class MasterProcedureReadSerializer(serializers.ModelSerializer):
    procedure = ProcedureSerializer()
    employee = EmployeeShortSerialiser()

    class Meta:
        model = MasterProcedure
        fields = (
            "procedure",
            "employee",
            "price",
            "coef",
            "created",
            "modified",
        )


class MasterProcedureWriteSerializer(serializers.ModelSerializer):
    employee = serializers.HiddenField(default=CurrentEmployeeDefault())

    class Meta(MasterProcedureReadSerializer.Meta):
        read_only_fields = ("created", "modified")
        validators = [
            UniqueTogetherValidator(
                queryset=MasterProcedure.objects.all(),
                fields=["procedure", "employee"],
            ),
        ]

    def to_representation(self, instance: MasterProcedure) -> dict:
        return MasterProcedureReadSerializer(instance).data
