import pytest

from app.types import GenericModelAssertion
from companies.api.serializers import CategorySerializer
from companies.models import Category
from companies.services import CategoryCreator

pytestmark = [pytest.mark.django_db]


def test_category_created_with_valid_data(category_data: dict, assert_category: GenericModelAssertion):
    serializer = CategorySerializer(data=category_data)

    assert_category(category_data, id=CategoryCreator(serializer)().id)


def test_category_does_not_duplicate(category_data: dict):
    serializer = CategorySerializer(data=category_data)
    for _ in range(2):
        CategoryCreator(serializer)()

    assert Category.objects.count() == 1
