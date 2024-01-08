import pytest

from app.types import ModelAssertion
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType
from companies.services import MaterialTypeCreator

pytestmark = [pytest.mark.django_db]


def test_material_type_is_created_with_valid_data(material_type_data: dict, assert_material_type: ModelAssertion):
    serializer = MaterialTypeSerializer(data=material_type_data)
    MaterialTypeCreator(serializer)()

    assert_material_type(material_type_data)


def test_material_type_do_not_duplicate(material_type_data: dict):
    serializer = MaterialTypeSerializer(data=material_type_data)
    for _ in range(2):
        MaterialTypeCreator(serializer)()

    assert MaterialType.objects.count() == 1
