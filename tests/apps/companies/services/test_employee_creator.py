import pytest

from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model

from app.types import GenericExistCheckAssertion, GenericModelAssertion
from companies.api.serializers import EmployeeSerializer
from companies.models import Employee
from companies.services import EmployeeCreator
from companies.types import EmployeeData

User = get_user_model()

pytestmark = [pytest.mark.django_db]


def test_employee_is_created_with_valid_data(
    employee_data: EmployeeData, assert_employee: GenericModelAssertion[EmployeeData]
):
    serializer = EmployeeSerializer(data=employee_data)

    assert_employee(employee_data, id=EmployeeCreator(serializer)().id)


def test_employee_is_not_created_with_invalid_data(
    employee_invalid_data: dict, assert_doesnt_exist: GenericExistCheckAssertion[type[Employee]]
):
    serializer = EmployeeSerializer(data=employee_invalid_data)

    with pytest.raises(ValidationError):
        EmployeeCreator(serializer)()
    assert_doesnt_exist(Employee)
