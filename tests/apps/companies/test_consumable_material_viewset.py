import pytest
from datetime import datetime
from rest_framework import status

from django.urls import reverse
from django.utils import timezone

from app.testing import StatusApiClient
from app.types import RestPageAssertion
from companies.api.serializers import ConsumableMateriaSerializer
from companies.models import Material, Point, StockMaterial
from purchases.models import UsedMaterial

pytestmark = [pytest.mark.django_db]


def test_point_non_managing_staff_cannot_read_materials(
    as_point_non_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
            },
        ),
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_managing_staff_can_read_materials(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
            },
        ),
    )


def test_point_managing_staff_cannot_read_materials_with_invalid_query_params(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
    material_date_query_params: dict[str, str],
):
    material_date_query_params["date_to"] = "2222"
    as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
            },
        ),
        expected_status=status.HTTP_400_BAD_REQUEST,
        data=material_date_query_params,
    )


def test_cosumable_materials_list(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
    assert_rest_page: RestPageAssertion,
):
    cosumable_materials = Material.objects.point(
        point_with_consumable_materials.company.id,
        point_with_consumable_materials.id,
        {},
    )
    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
            },
        ),
    )
    assert_rest_page(response, cosumable_materials, ConsumableMateriaSerializer)


def test_cosumable_materials_detail(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    cosumable_material = Material.objects.point(
        point_with_consumable_materials.company.id,
        point_with_consumable_materials.id,
        {},
    ).first()
    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-detail",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
                "pk": cosumable_material.id,  # type: ignore[union-attr]
            },
        ),
    )
    assert response == ConsumableMateriaSerializer(cosumable_material).data


def test_consumable_materials_usage_and_stocks_sort_by_date(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    material = Material.objects.first()

    assert material

    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-detail",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
                "pk": material.id,
            },
        ),
    )
    for movement in [response["stocks"], response["usage"]]:
        assert movement
        assert all(elem1["date"] < elem2["date"] for elem1, elem2 in zip(movement, movement[1:]))


def test_consumable_materials_usage_and_stocks_filter_by_date(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
    material_date_query_params: dict[str, str],
):
    def get_date(date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d")

    material = Material.objects.first()

    assert material
    params = material_date_query_params
    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-detail",
            kwargs={
                "company_pk": point_with_consumable_materials.company.id,
                "point_pk": point_with_consumable_materials.id,
                "pk": material.id,
            },
        ),
        data=params,
    )
    for movement in [response["stocks"], response["usage"]]:
        assert movement
        assert all(
            get_date(params["date_from"]) <= get_date(elem["date"]) <= get_date(params["date_to"]) for elem in movement
        )


def test_consumable_materials_amount(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    material = Material.objects.first()

    assert material

    url = reverse(
        "api_v1:companies:consumable-material-detail",
        kwargs={
            "company_pk": point_with_consumable_materials.company.id,
            "point_pk": point_with_consumable_materials.id,
            "pk": material.id,
        },
    )
    response = as_point_managing_staff.get(url)  # type: ignore[no-untyped-call]
    stock_material = StockMaterial.objects.filter(material_id=material.id).order_by("stock__date").first()

    assert stock_material

    stock_material.stock.date = timezone.now().date()
    stock_material.stock.save()
    new_response = as_point_managing_staff.get(url)  # type: ignore[no-untyped-call]

    assert int(response["stocks"][0]["amount"]) - stock_material.quantity == int(new_response["stocks"][0]["amount"])


def test_consumable_materials_usage_amount(
    as_point_managing_staff: StatusApiClient,
    point_with_consumable_materials: Point,
):
    material = Material.objects.first()

    assert material

    url = reverse(
        "api_v1:companies:consumable-material-detail",
        kwargs={
            "company_pk": point_with_consumable_materials.company.id,
            "point_pk": point_with_consumable_materials.id,
            "pk": material.id,
        },
    )
    response = as_point_managing_staff.get(url)  # type: ignore[no-untyped-call]
    used_material = UsedMaterial.objects.filter(material__material_id=material.id).order_by("created").first()

    assert used_material

    used_material.created = timezone.now()
    used_material.save()
    new_response = as_point_managing_staff.get(url)  # type: ignore[no-untyped-call]

    assert int(response["usage"][0]["amount"]) - used_material.amount == int(new_response["usage"][0]["amount"])
