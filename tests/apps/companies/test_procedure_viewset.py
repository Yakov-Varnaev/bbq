import pytest
from typing import Any

from rest_framework import status

from django.urls import reverse

from app.testing import ApiClient, FixtureFactory, StatusApiClient
from app.types import ExistCheckAssertion, ModelAssertion, RestPageAssertion
from companies.api.serializers import ProcedureSerializer
from companies.models import Category, Department, Procedure

pytestmark = [pytest.mark.django_db]


def test_point_managing_staff_can_create_procedure(
    as_point_managing_staff: ApiClient,
    category: Category,
    procedure_data: dict[str, Any],
    procedure_reverse_kwargs: dict[str, Any],
    assert_procedure: ModelAssertion,
):
    response = as_point_managing_staff.post(reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs), procedure_data)  # type: ignore[no-untyped-call]

    assert_procedure(procedure_data, category=category)
    assert response == ProcedureSerializer(Procedure.objects.get(**procedure_data)).data


def test_non_point_managing_staff_cannot_create_procedure(
    as_point_non_managing_staff: StatusApiClient,
    procedure_data: dict[str, Any],
    procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs),
        procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_doesnt_exist(Procedure)


@pytest.mark.parametrize("pk", ["company_pk", "point_pk", "department_pk"])
def test_create_procedure_with_non_existing_company_or_point_or_department(
    pk: str,
    as_point_managing_staff: ApiClient,
    procedure_data: dict[str, Any],
    procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    procedure_reverse_kwargs[pk] = 999
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs),
        procedure_data,
        expected_status=status.HTTP_404_NOT_FOUND,
    )

    assert_doesnt_exist(Procedure)


@pytest.mark.parametrize("invalid_data", [{"name": ""}])
def test_create_procedure_invalid_data(
    as_point_managing_staff: ApiClient,
    factory: FixtureFactory,
    procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
    invalid_data: dict[str, str],
):
    procedure_data = factory.procedure_data(**invalid_data)
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs),
        procedure_data,
        expected_status=status.HTTP_400_BAD_REQUEST,
    )

    assert_doesnt_exist(Procedure)


def test_department_field_is_ignored_on_procedure_creation(
    as_point_managing_staff: ApiClient,
    category: Category,
    factory: FixtureFactory,
    procedure_data: dict[str, Any],
    procedure_reverse_kwargs: dict[str, Any],
    assert_procedure: ModelAssertion,
):
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs),
        procedure_data | {"department": factory.department().id},
        expected_status=status.HTTP_201_CREATED,
    )

    assert_procedure(procedure_data, category=category)


def test_procedure_list(
    reader_client: ApiClient,
    factory: FixtureFactory,
    category: Category,
    department: Department,
    procedure_reverse_kwargs: dict[str, Any],
    assert_rest_page: RestPageAssertion,
):
    procedures = sorted(factory.cycle(5).procedure(category=category, department=department), key=lambda d: d.name)
    response = reader_client.get(reverse("api_v1:companies:procedure-list", kwargs=procedure_reverse_kwargs))  # type: ignore[no-untyped-call]

    assert_rest_page(response, procedures, ProcedureSerializer)


def test_procedure_detail(reader_client: ApiClient, procedure: Procedure):
    response = reader_client.get(procedure.get_absolute_url())  # type: ignore[no-untyped-call]

    assert response == ProcedureSerializer(procedure).data


def test_point_managing_staff_can_update_procedure(
    as_point_managing_staff: ApiClient,
    procedure: Procedure,
    category: Category,
    procedure_data: dict[str, Any],
    assert_procedure: ModelAssertion,
):
    response = as_point_managing_staff.put(procedure.get_absolute_url(), procedure_data)  # type: ignore[no-untyped-call]
    procedure.refresh_from_db()

    assert_procedure(procedure_data, category=category)
    assert response == ProcedureSerializer(Procedure.objects.get(**procedure_data)).data


def test_point_non_managing_staff_cannot_update_procedure(
    as_point_non_managing_staff: StatusApiClient,
    procedure: Procedure,
    procedure_data: dict[str, Any],
):
    as_point_non_managing_staff.put(  # type: ignore[no-untyped-call]
        procedure.get_absolute_url(),
        procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )


@pytest.mark.parametrize("invalid_data", [{"name": ""}])
def test_update_procedure_invalid_data(
    as_point_managing_staff: ApiClient,
    procedure: Procedure,
    factory: FixtureFactory,
    invalid_data: dict[str, str],
):
    procedure_data = factory.procedure_data(**invalid_data)
    as_point_managing_staff.put(procedure.get_absolute_url(), procedure_data, expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore[no-untyped-call]


def test_point_managing_staff_can_delete_procedure(
    as_point_managing_staff: ApiClient,
    procedure: Procedure,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_managing_staff.delete(procedure.get_absolute_url())  # type: ignore[no-untyped-call]

    assert_doesnt_exist(Procedure)


def test_point_non_managing_staff_cannot_delete_procedure(
    as_point_non_managing_staff: StatusApiClient,
    procedure: Procedure,
    assert_exists: ExistCheckAssertion,
):
    as_point_non_managing_staff.delete(  # type: ignore[no-untyped-call]
        procedure.get_absolute_url(),
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_exists(Procedure)
