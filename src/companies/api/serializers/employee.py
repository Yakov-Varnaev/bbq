from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

from companies.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    def validate_departments(self, departments: list[int]) -> list[int]:
        if len(set(departments)) != len(departments):
            raise ValidationError(_("departments duplication"))
        return departments

    class Meta:
        model = Employee
        fields = "__all__"
