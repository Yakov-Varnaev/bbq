import pytest

from rest_framework import status

from django.urls import reverse

from app.testing import StatusApiClient
from app.types import RestPageAssertion
from companies.api.serializers import ConsumableMateriaSerializer
from companies.models import Company, Material, Point

pytestmark = [pytest.mark.django_db]


def test_point_non_managing_staff_cannot_read_materials(
    as_point_non_managing_staff: StatusApiClient,
    company: Company,
    company_point: Point,
):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
        ),
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_managing_staff_can_read_materials(
    as_point_managing_staff: StatusApiClient,
    company: Company,
    company_point: Point,
):
    as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
        ),
    )


def test_point_managing_staff_cannot_read_materials_with_invalid_query_params(
    as_point_managing_staff: StatusApiClient,
    company: Company,
    company_point: Point,
    material_date_query_params: dict[str, str],
):
    material_date_query_params["date_to"] = "2222"
    as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
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
