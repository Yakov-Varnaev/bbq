from typing import TypedDict

from typing_extensions import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from companies.models.stock import Material, Stock


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
            "material": material.id,  # type: ignore[union-attr]
            "quantity": self.field("random.randint", a=1, b=100),
            "price": self.field("random.randint", a=1, b=100),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}


@register
def stock_material(self: FixtureFactory, **kwargs: dict) -> dict:
    return self.mixer.blend("companies.StockMaterial", **kwargs)
