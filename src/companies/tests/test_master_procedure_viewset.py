import pytest
from typing import Any

from freezegun import freeze_time
from rest_framework import status

from django.urls import reverse
from django.utils import timezone

from app.testing import ApiClient, FixtureFactory, StatusApiClient
from app.types import ExistCheckAssertion, ModelAssertion, RestPageAssertion
from companies.api.serializers import MasterProcedureSerializer
from companies.models import Employee, MasterProcedure, Procedure

pytestmark = [pytest.mark.django_db]


def test_point_managing_staff_can_create_master_procedure(
    as_point_managing_staff: ApiClient,
    employee: Employee,
    procedure: Procedure,
    master_procedure_reverse_kwargs: dict[str, Any],
    master_procedure_data: dict[str, Any],
    assert_master_procedure: ModelAssertion,
):
    response = as_point_managing_staff.post(reverse("api_v1:companies:master-procedure-list", kwargs=master_procedure_reverse_kwargs), master_procedure_data)  # type: ignore[no-untyped-call]

    assert_master_procedure(master_procedure_data, employee=employee, procedure=procedure)
    assert response == MasterProcedureSerializer(MasterProcedure.objects.get(**master_procedure_data)).data


def test_point_managing_staff_cannot_create_duplicate_master_procedure(
    as_point_managing_staff: ApiClient,
    master_procedure_reverse_kwargs: dict[str, Any],
    master_procedure_data: dict[str, Any],
):
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:master-procedure-list",
            kwargs=master_procedure_reverse_kwargs,
        ),
        master_procedure_data,
        expected_status=status.HTTP_201_CREATED,
    )
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:master-procedure-list",
            kwargs=master_procedure_reverse_kwargs,
        ),
        master_procedure_data,
        expected_status=status.HTTP_400_BAD_REQUEST,
    )
    assert MasterProcedure.objects.count() == 1


def test_non_point_managing_staff_cannot_create_master_procedure(
    as_point_non_managing_staff: StatusApiClient,
    master_procedure_data: dict[str, Any],
    master_procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:master-procedure-list", kwargs=master_procedure_reverse_kwargs),
        master_procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_doesnt_exist(MasterProcedure)


@pytest.mark.parametrize("pk", ["company_pk", "point_pk", "employee_pk"])
def test_create_master_procedure_with_non_existing_company_or_point_or_employee(
    pk: str,
    as_point_managing_staff: ApiClient,
    master_procedure_data: dict[str, Any],
    master_procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
):
    master_procedure_reverse_kwargs[pk] = 999
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:master-procedure-list", kwargs=master_procedure_reverse_kwargs),
        master_procedure_data,
        expected_status=status.HTTP_404_NOT_FOUND,
    )

    assert_doesnt_exist(MasterProcedure)


@pytest.mark.parametrize("invalid_data", [{"coef": -0.1}, {"coef": 1.1}])
def test_create_master_procedure_invalid_data(
    as_point_managing_staff: ApiClient,
    factory: FixtureFactory,
    employee: Employee,
    procedure: Procedure,
    master_procedure_reverse_kwargs: dict[str, Any],
    assert_doesnt_exist: ExistCheckAssertion,
    invalid_data: dict[str, str],
):
    as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse("api_v1:companies:master-procedure-list", kwargs=master_procedure_reverse_kwargs),
        factory.master_procedure_data(employee=employee.id, procedure=procedure.id, **invalid_data),
        expected_status=status.HTTP_400_BAD_REQUEST,
    )

    assert_doesnt_exist(MasterProcedure)


def test_master_procedure_list(
    reader_client: ApiClient,
    factory: FixtureFactory,
    procedure: Procedure,
    employee: Employee,
    master_procedure_reverse_kwargs: dict[str, Any],
    assert_rest_page: RestPageAssertion,
):
    master_procedures = factory.cycle(5).master_procedure(procedure=procedure, employee=employee)
    response = reader_client.get(reverse("api_v1:companies:master-procedure-list", kwargs=master_procedure_reverse_kwargs))  # type: ignore[no-untyped-call]

    assert_rest_page(response, master_procedures, MasterProcedureSerializer, None, None)


def test_master_procedure_detail(reader_client: ApiClient, master_procedure: MasterProcedure):
    assert reader_client.get(master_procedure.get_absolute_url()) == MasterProcedureSerializer(master_procedure).data  # type: ignore[no-untyped-call]


def test_point_managing_staff_can_update_master_procedure(
    as_point_managing_staff: ApiClient,
    master_procedure: Procedure,
    procedure: Procedure,
    employee: Employee,
    master_procedure_data: dict[str, Any],
    assert_master_procedure: ModelAssertion,
):
    response = as_point_managing_staff.put(master_procedure.get_absolute_url(), master_procedure_data)  # type: ignore[no-untyped-call]
    master_procedure.refresh_from_db()

    assert_master_procedure(master_procedure_data, procedure=procedure, employee=employee)
    assert response == MasterProcedureSerializer(MasterProcedure.objects.get(**master_procedure_data)).data


def test_point_non_managing_staff_cannot_update_master_procedure(
    as_point_non_managing_staff: StatusApiClient,
    master_procedure: MasterProcedure,
    master_procedure_data: dict[str, Any],
):
    as_point_non_managing_staff.put(  # type: ignore[no-untyped-call]
        master_procedure.get_absolute_url(),
        master_procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )


@pytest.mark.parametrize("invalid_data", [{"coef": -0.1}, {"coef": 1.1}])
def test_update_master_procedure_invalid_data(
    as_point_managing_staff: ApiClient,
    master_procedure: MasterProcedure,
    factory: FixtureFactory,
    employee: Employee,
    procedure: Procedure,
    invalid_data: dict[str, str],
):
    as_point_managing_staff.put(  # type: ignore[no-untyped-call]
        master_procedure.get_absolute_url(),
        factory.master_procedure_data(employee=employee.id, procedure=procedure.id, **invalid_data),
        expected_status=status.HTTP_400_BAD_REQUEST,
    )


@freeze_time()
def test_point_managing_staff_can_delete_master_procedure(
    as_point_managing_staff: ApiClient,
    master_procedure: MasterProcedure,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_managing_staff.delete(master_procedure.get_absolute_url())  # type: ignore[no-untyped-call]

    assert_doesnt_exist(MasterProcedure)
    assert MasterProcedure.include_archived.filter(archived=timezone.now()).exists()


@freeze_time()
def test_point_non_managing_staff_cannot_delete_procedure(
    as_point_non_managing_staff: StatusApiClient,
    master_procedure: MasterProcedure,
    assert_exists: ExistCheckAssertion,
):
    as_point_non_managing_staff.delete(  # type: ignore[no-untyped-call]
        master_procedure.get_absolute_url(),
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_exists(MasterProcedure)
    assert not MasterProcedure.include_archived.filter(archived=timezone.now()).exists()


@freeze_time()
def test_master_procedure_can_restore(
    as_point_managing_staff: ApiClient,
    master_procedure: MasterProcedure,
    assert_exists: ExistCheckAssertion,
):
    as_point_managing_staff.delete(master_procedure.get_absolute_url())  # type: ignore[no-untyped-call]

    archived_master_procedure = MasterProcedure.include_archived.get(archived=timezone.now())
    archived_master_procedure.restore()
    assert_exists(MasterProcedure)