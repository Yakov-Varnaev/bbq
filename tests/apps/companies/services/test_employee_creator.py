import pytest

from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model

from app.types import ExistCheckAssertion, GenericModelAssertion
from companies.api.serializers import EmployeeSerializer
from companies.models.employee import Employee
from companies.services import EmployeeCreator

User = get_user_model()

pytestmark = [pytest.mark.django_db]


def test_employee_is_created_with_valid_data(employee_data: dict, assert_employee: GenericModelAssertion):
    serializer = EmployeeSerializer(data=employee_data)

    assert_employee(employee_data, id=EmployeeCreator(serializer)().id)


def test_employee_is_not_created_with_invalid_data(
    employee_invalid_data: dict, assert_doesnt_exist: ExistCheckAssertion
):
    serializer = EmployeeSerializer(data=employee_invalid_data)

    with pytest.raises(ValidationError):
        EmployeeCreator(serializer)()
    assert_doesnt_exist(Employee)
