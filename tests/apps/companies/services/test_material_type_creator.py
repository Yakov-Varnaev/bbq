import pytest

from app.types import GenericModelAssertion
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType
from companies.services import MaterialTypeCreator

pytestmark = [pytest.mark.django_db]


def test_material_type_is_created_with_valid_data(material_type_data: dict, assert_material_type: GenericModelAssertion):
    serializer = MaterialTypeSerializer(data=material_type_data)

    assert_material_type(material_type_data, id=MaterialTypeCreator(serializer)().id)


def test_material_type_does_not_duplicate(material_type_data: dict):
    serializer = MaterialTypeSerializer(data=material_type_data)
    for _ in range(2):
        MaterialTypeCreator(serializer)()

    assert MaterialType.objects.count() == 1
