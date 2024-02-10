import pytest
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.urls import reverse

from app.testing import ApiClient, FixtureFactory
from app.types import GenericExistCheckAssertion, GenericModelAssertion, RestPageAssertion
from companies.api.fields import LowercaseCharField
from companies.api.serializers import MaterialTypeSerializer
from companies.models import MaterialType
from companies.types import MaterialTypeData

pytestmark = pytest.mark.django_db


def test_unauthorized_users_cannot_create_material_type(as_anon: ApiClient, material_type_data: dict):
    url = reverse("api_v1:companies:material-types-list")
    as_anon.post(url, data=material_type_data, expected_status=status.HTTP_401_UNAUTHORIZED)  # type: ignore

    assert not MaterialType.objects.exists()


def test_authenticated_user_can_create_material_type(
    as_user: ApiClient,
    material_type_data: MaterialTypeData,
    assert_material_type: GenericModelAssertion[MaterialTypeData],
):
    url = reverse("api_v1:companies:material-types-list")
    as_user.post(url, data=material_type_data, expected_status=status.HTTP_201_CREATED)  # type: ignore
    material_type = MaterialType.objects.filter(**material_type_data)

    assert material_type.exists()
    assert_material_type(data=material_type_data, id=material_type.get().id)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_material_type_create_invalid_data(
    as_user: ApiClient,
    factory: FixtureFactory,
    invalid_fields: dict[str, Any],
    assert_doesnt_exist: GenericExistCheckAssertion[type[MaterialType]],
):
    url = reverse("api_v1:companies:material-types-list")
    as_user.post(url, data=factory.material_type_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore

    assert_doesnt_exist(MaterialType)


def test_material_type_retrieve(reader_client: ApiClient, material_type: MaterialType):
    url = reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk})
    material_type_data = reader_client.get(url)  # type: ignore

    assert MaterialTypeSerializer(material_type).data == material_type_data


def test_material_type_list(reader_client: ApiClient, factory: FixtureFactory, assert_rest_page: RestPageAssertion):
    factory.cycle(5).material_type()
    url = reverse("api_v1:companies:material-types-list")
    material_type_data = reader_client.get(url)  # type: ignore

    assert_rest_page(material_type_data, MaterialType.objects.all(), MaterialTypeSerializer)


def test_superuser_can_update_material_type(
    as_superuser: ApiClient,
    material_type: MaterialType,
    assert_material_type: GenericModelAssertion[MaterialTypeData],
    factory: FixtureFactory,
):
    url = reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk})
    material_type_data = factory.material_type_data()
    response_data = as_superuser.put(url, data=material_type_data)  # type: ignore
    material_type.refresh_from_db()

    assert MaterialTypeSerializer(material_type).data == response_data
    assert_material_type(material_type_data, id=material_type.id)


@pytest.mark.parametrize("invalid_fields", [{"name": ""}])
def test_udpate_material_type_invalid_data(
    as_superuser: ApiClient, material_type: MaterialType, factory: FixtureFactory, invalid_fields: dict[str, str]
):
    url = reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk})
    response = as_superuser.put(url, data=factory.material_type_data(**invalid_fields), expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore

    assert response.get("name") == [LowercaseCharField.default_error_messages.get("blank")]


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def terst_unauthorized_users_cannot_update_material_type(
    client: ApiClient, expected_status: int, material_type: MaterialType, material_type_data: dict
):
    expected_data = MaterialTypeSerializer(material_type).data
    url = reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk})
    client.put(url, data=material_type_data, expected_status=expected_status)  # type: ignore
    material_type.refresh_from_db()

    assert MaterialTypeSerializer(material_type).data == expected_data


@pytest.mark.parametrize(
    ("client", "expected_status"),
    [
        (lf("as_user"), status.HTTP_403_FORBIDDEN),
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED),
    ],
)
def test_only_super_user_can_delete_material_type(client: ApiClient, expected_status: int, material_type: MaterialType):
    url = reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk})
    client.delete(url, expected_status=expected_status)  # type: ignore

    assert MaterialType.objects.count()


def test_name_field_is_in_lowercase(as_superuser: ApiClient, material_type_data: dict):
    lower_name_material_type = material_type_data["name"].lower()
    material_type_data["name"] = material_type_data["name"].upper()
    post_response = as_superuser.post(reverse("api_v1:companies:material-types-list"), data=material_type_data)  # type: ignore
    material_type = MaterialType.objects.get(name=lower_name_material_type)
    get_response = as_superuser.get(reverse("api_v1:companies:material-types-detail", kwargs={"pk": material_type.pk}))  # type: ignore

    assert post_response.get("name") == lower_name_material_type
    assert material_type.name == lower_name_material_type
    assert get_response.get("name") == lower_name_material_type
