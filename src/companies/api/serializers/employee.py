from typing import Any

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from django.utils.translation import gettext_lazy as _

from companies.api.serializers import CurrentEmployeeDefault
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
    employee = serializers.HiddenField(default=CurrentEmployeeDefault())

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

    def to_representation(self, instance: MasterProcedure) -> dict[str, Any]:
        data = super().to_representation(instance)
        data["employee"] = {
            "first_name": instance.employee.user.first_name,
            "last_name": instance.employee.user.last_name,
            "id": instance.employee.id,
        }
        data["procedure"] = {
            "name": instance.procedure.name,
            "category": instance.procedure.category.name,
        }
        return data
