import pytest

from django.utils import timezone

from app.testing.factory import FixtureFactory
from purchases.models.product_material import ProductMaterial

pytestmark = pytest.mark.django_db


def test_deleted_product_materials_are_not_included_by_default(factory: FixtureFactory):
    factory.product_material()
    factory.product_material(deleted=timezone.now())

    assert ProductMaterial.objects.count() == 1
