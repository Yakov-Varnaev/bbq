from typing import TypedDict

from typing_extensions import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from companies.models.department import Department
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
