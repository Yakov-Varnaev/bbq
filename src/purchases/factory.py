from app.testing import register
from app.testing.factory import FixtureFactory
from purchases.models.product_material import ProductMaterial


@register
def product_material(self: FixtureFactory, **kwargs) -> ProductMaterial:
    return self.mixer.blend(ProductMaterial, **kwargs)
