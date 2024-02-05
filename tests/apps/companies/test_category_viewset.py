import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing import ApiClient, FixtureFactory
from app.types import ExistCheckAssertion, ModelAssertion, RestPageAssertion
from companies.api.fields import LowercaseCharField
from companies.api.serializers import CategorySerializer
from companies.models import Category

pytestmark = pytest.mark.django_db


def test_unauthorized_users_cannot_create_category(as_anon: ApiClient, category_data: dict):
    url = reverse("api_v1:companies:category-list")
    as_anon.post(url, data=category_data, expected_status=status.HTTP_401_UNAUTHORIZED)  # type: ignore

    assert not Category.objects.exists()


def test_authenticated_user_can_create_category(
    as_user: ApiClient,
    category_data: dict,
    assert_category: ModelAssertion,
):
    url = reverse("api_v1:companies:category-list")
    as_user.post(url, data=category_data, expected_status=status.HTTP_201_CREATED)  # type: ignore

    assert Category.objects.exists()
    assert_category(data=category_data)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_category_create_invalid_data(
    as_user: ApiClient,
    factory: FixtureFactory,
    invalid_fields: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    url = reverse("api_v1:companies:category-list")
    as_user.post(url, data=factory.category_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore

    assert_doesnt_exist(Category)


def test_category_retrieve(reader_client: ApiClient, category: Category):
    category_data = reader_client.get(reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk}))  # type: ignore

    assert CategorySerializer(category).data == category_data


def test_category_list(reader_client: ApiClient, factory: FixtureFactory, assert_rest_page: RestPageAssertion):
    factory.cycle(5).category()
    category_data = reader_client.get(reverse("api_v1:companies:category-list"))  # type: ignore

    assert_rest_page(category_data, Category.objects.all(), CategorySerializer)


def test_superuser_can_update_category(
    as_superuser: ApiClient, category: Category, assert_category: ModelAssertion, factory: FixtureFactory
):
    url = reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk})
    category_data = factory.category_data()
    response_data = as_superuser.put(url, data=category_data)  # type: ignore
    category.refresh_from_db()

    assert CategorySerializer(category).data == response_data
    assert_category(category_data)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_udpate_category_invalid_data(
    as_superuser: ApiClient, category: Category, factory: FixtureFactory, invalid_fields: dict[str, str]
):
    url = reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk})
    response = as_superuser.put(url, data=factory.category_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore

    assert response.get("name") == [LowercaseCharField.default_error_messages.get("blank")]


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def terst_unauthorized_users_cannot_update_category(
    client: ApiClient, expected_status: int, category: Category, category_data: dict
):
    expected_data = CategorySerializer(category).data
    url = reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk})
    client.put(url, data=category_data, expected_status=expected_status)  # type: ignore
    category.refresh_from_db()

    assert CategorySerializer(category).data == expected_data


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_only_super_user_can_delete_category(client: ApiClient, expected_status: int, category: Category):
    url = reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk})
    client.delete(url, expected_status=expected_status)  # type: ignore

    assert Category.objects.count()


def test_name_field_is_in_lowercase(as_superuser: ApiClient, category_data: dict):
    lower_name_category = category_data["name"].lower()
    category_data["name"] = category_data["name"].upper()
    post_response = as_superuser.post(reverse("api_v1:companies:category-list"), data=category_data)  # type: ignore
    category = Category.objects.get(name=lower_name_category)
    get_response = as_superuser.get(reverse("api_v1:companies:category-detail", kwargs={"pk": category.pk}))  # type: ignore

    assert post_response.get("name") == lower_name_category
    assert category.name == lower_name_category
    assert get_response.get("name") == lower_name_category
