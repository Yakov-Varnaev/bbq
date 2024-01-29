from typing import Any

from app.testing import register
from app.testing.factory import FixtureFactory
from purchases.models.product_material import ProductMaterial


@register
def product_material_data(self: FixtureFactory, **kwargs: Any) -> dict:
    material = kwargs.pop("material", None)
    if material:
        kwargs["material"] = material.id
    else:
        kwargs["material"] = self.stock_material().id
    return {
        "price": self.mixer.faker.pydecimal(left_digits=2, right_digits=2, positive=True),
        **kwargs,
    }


@register
def product_material(self: FixtureFactory, **kwargs: Any) -> ProductMaterial:
    return self.mixer.blend(ProductMaterial, **kwargs)
