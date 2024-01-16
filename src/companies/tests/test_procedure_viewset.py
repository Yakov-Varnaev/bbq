import pytest
from typing import Any

from django.urls import reverse

from app.testing import ApiClient, StatusApiClient
from app.types import ExistCheckAssertion, ModelAssertion
from companies.api.serializers import ProcedureSerializer
from companies.models import MaterialType, Procedure

pytestmark = [pytest.mark.django_db]


def test_point_managing_staff_can_create_procedures(
    as_point_managing_staff: ApiClient,
    material_type: MaterialType,
    procedure_data: dict[str, Any],
    procedure_kwargs: dict[str, Any],
    assert_procedure: ModelAssertion,
):
    response = as_point_managing_staff.post(reverse("api_v1:companies:procedure-list", kwargs=procedure_kwargs), procedure_data)  # type: ignore[no-untyped-call]

    assert_procedure(procedure_data, kind=material_type)
    assert response == ProcedureSerializer(Procedure.objects.get(**procedure_data)).data


def test_non_point_managing_staff_cannot_create_procedures(
    as_point_non_managing_staff: StatusApiClient,
    procedure_data: dict[str, Any],
    procedure_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:procedure-list", kwargs=procedure_kwargs),
        procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_doesnt_exist(Procedure)
