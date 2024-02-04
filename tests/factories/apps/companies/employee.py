from typing import TypedDict

from typing_extensions import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from companies.models import Department, Employee, MasterProcedure
from users.models import User


class EmployeeData(TypedDict, total=False):
    departments: list[int | Department]
    user: int | User


@register
def employee_data(self: FixtureFactory, **kwargs: Unpack[EmployeeData]) -> dict:
    departments = kwargs.pop("departments", None)
    user = kwargs.pop("user", None)
    if departments is None:
        departments = [self.department()]
    if user is None:
        user = self.user()
    return {
        "user": user if isinstance(user, int) else user.pk,
        "departments": [department if isinstance(department, int) else department.pk for department in departments],
        "position": self.field("text.word"),
    }


@register
def employee(self: FixtureFactory, **kwargs: dict) -> Employee:
    return self.mixer.blend(Employee, **kwargs)


@register
def master_procedure_data(self: FixtureFactory, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"price": self.field("random.randint", a=1, b=99999)},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def master_procedure(self: FixtureFactory, **kwargs: dict) -> MasterProcedure:
    return self.mixer.blend(MasterProcedure, **kwargs)
