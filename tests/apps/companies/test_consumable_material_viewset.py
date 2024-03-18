import pytest

from rest_framework import status

from django.urls import reverse

from app.testing import ApiClient
from companies.models import Company, Point

pytestmark = [pytest.mark.django_db]


def test_point_non_managing_staff_cannot_read_materials(
    as_point_non_managing_staff: ApiClient,
    company: Company,
    company_point: Point,
):
    as_point_non_managing_staff.get(
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
        ),
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_managing_staff_can_read_materials(
    as_point_managing_staff: ApiClient,
    company: Company,
    company_point: Point,
):
    as_point_managing_staff.get(
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
        ),
    )


def test_point_managing_staff_cannot_read_materials_with_invalid_query_params(
    as_point_managing_staff: ApiClient,
    company: Company,
    company_point: Point,
    material_date_query_params: dict[str, str],
):
    material_date_query_params["date_to"] = "2222"
    as_point_managing_staff.get(
        reverse(
            "api_v1:companies:consumable-material-list",
            kwargs={"company_pk": company.id, "point_pk": company_point.id},
        ),
        expected_status=status.HTTP_400_BAD_REQUEST,
        data=material_date_query_params,
    )
