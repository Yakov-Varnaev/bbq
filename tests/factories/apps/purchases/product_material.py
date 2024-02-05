from faker import Faker
from typing_extensions import Unpack

from app.testing.factory import FixtureFactory, register
from purchases.models.product_material import ProductMaterial
from purchases.types import ProductMaterialData

faker = Faker()


@register
def product_material_data(self: FixtureFactory, **kwargs: Unpack[ProductMaterialData]) -> ProductMaterialData:
    material = kwargs.pop("material", None)
    if material is None:
        material = self.stock_material()
    schema = self.schema(
        schema=lambda: {
            "material": material.id,
            "price": faker.pydecimal(left_digits=8, right_digits=2, positive=True),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}  # type: ignore[typeddict-item]


@register
def product_material(self: FixtureFactory, **kwargs: Unpack[ProductMaterialData]) -> ProductMaterial:
    return self.mixer.blend(ProductMaterial, **kwargs)
