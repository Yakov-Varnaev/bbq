from typing import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from purchases.models import UsedMaterial
from purchases.types import UsedMaterialData


@register
def used_material_data(self: FixtureFactory, **kwargs: Unpack[UsedMaterialData]) -> UsedMaterialData:
    procedure = kwargs.pop("procedure", None)
    if procedure is None:
        procedure = self.procedure()
    material = kwargs.pop("material", None)
    if material is None:
        material = self.stock_material()
    schema = self.schema(
        schema=lambda: {
            "procedure": procedure.id,
            "material": material.id,
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}  # type: ignore[typeddict-item]


@register
def used_material(self: FixtureFactory, **kwargs: Unpack[UsedMaterialData]) -> UsedMaterial:
    return self.mixer.blend(UsedMaterial, **kwargs)
