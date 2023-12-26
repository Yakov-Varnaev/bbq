from typing import TypedDict

from typing_extensions import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from app.testing.types import FactoryProtocol
from companies.models import Company, Point
from companies.models.department import Department
from companies.models.stock import Material, Stock
from users.models import User


@register
def company(self: FactoryProtocol, **kwargs: dict) -> Company:
    return self.mixer.blend(Company, **kwargs)


@register
def company_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def company_point_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {
            "address": self.field("address"),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def company_point(self: FactoryProtocol, **kwargs: dict) -> Point:
    return self.mixer.blend(Point, **kwargs)


@register
def department_data(self: FactoryProtocol, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def department(self: FactoryProtocol, **kwargs: dict) -> Department:
    return self.mixer.blend(Department, **kwargs)


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
def material(self: FixtureFactory, **kwargs: dict) -> dict:
    return self.mixer.blend(Material, **kwargs)


@register
def stock_data(self: FixtureFactory, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {
            "date": self.field("date"),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def stock(self: FixtureFactory, **kwargs: dict) -> dict:
    return self.mixer.blend(Stock, **kwargs)


class StockMaterialData(TypedDict, total=False):
    material: Material
    quantity: int
    price: int


@register
def stock_material_data(self: FixtureFactory, **kwargs: Unpack[StockMaterialData]) -> dict:
    material = kwargs.pop("material", None)
    if material is None:
        material = self.stock_material()
    schema = self.schema(
        schema=lambda: {
            "material": material.id,
            "quantity": self.field("random.randint", a=1, b=100),
            "price": self.field("random.randint", a=1, b=100),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def stock_material(self: FixtureFactory, **kwargs: dict) -> dict:
    return self.mixer.blend("companies.StockMaterial", **kwargs)
