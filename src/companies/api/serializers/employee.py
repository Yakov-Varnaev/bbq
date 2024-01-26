from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from django.utils.translation import gettext_lazy as _

from companies.models import Employee, MasterProcedure


class EmployeeSerializer(serializers.ModelSerializer):
    def validate_departments(self, departments: list[int]) -> list[int]:
        if len(set(departments)) != len(departments):
            raise ValidationError(_("departments duplication"))
        return departments

    class Meta:
        model = Employee
        fields = "__all__"


class MasterProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterProcedure
        fields = (
            "procedure",
            "employee",
            "price",
            "coef",
            "archived",
            "created",
            "modified",
        )
        read_only_fields = ("created", "modified")
        validators = [
            UniqueTogetherValidator(
                queryset=MasterProcedure.objects.all(),
                fields=["procedure", "employee"],
            ),
        ]
