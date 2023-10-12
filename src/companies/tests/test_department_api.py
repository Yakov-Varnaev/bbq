import pytest

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated

from django.urls import reverse

from app.api.permissions import IsCompanyOwnerOrReadOnly
from app.testing.api import ApiClient
from app.testing.factory import FixtureFactory
from app.typing import ExistCheckAssertion, ModelAssertion, RestPageAssertion
from companies.api.serializers import DepartmentSerializer
from companies.models import Department, Point

pytestmark = [pytest.mark.django_db]

non_point_managing_users_parametrization = (
    ("client", "status_code", "message"),
    [
        (lf("as_anon"), status.HTTP_401_UNAUTHORIZED, NotAuthenticated.default_detail),
        (lf("as_user"), status.HTTP_403_FORBIDDEN, IsCompanyOwnerOrReadOnly.message),
        (lf("as_another_company_owner"), status.HTTP_403_FORBIDDEN, IsCompanyOwnerOrReadOnly.message),
    ],
)


def test_point_managing_staff_can_create_departments(
    as_point_managing_staff: ApiClient,
    department_data: dict,
    company_point: Point,
    assert_department: ModelAssertion,
):
    response = as_point_managing_staff.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_point.company.id, "point_pk": company_point.id},
        ),
        department_data,
    )

    assert_department(department_data, point=company_point)
    assert response == DepartmentSerializer(Department.objects.first()).data


@pytest.mark.parametrize(*non_point_managing_users_parametrization)
def test_non_point_managing_staff_cannot_create_departments(
    client: ApiClient,
    status_code: int,
    message: str,
    department_data: dict,
    company_point: Point,
    assert_doesnt_exist: ExistCheckAssertion,
):
    response = client.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_point.company.id, "point_pk": company_point.id},
        ),
        department_data,
        expected_status=status_code,
    )

    assert_doesnt_exist(Department)
    assert response == {"detail": message}


@pytest.mark.parametrize(
    ("company_id", "point_id"),
    [
        (999, 999),
        (lf("company_pk"), 999),
        (999, lf("company_point_pk")),
    ],
)
def test_create_department_with_non_existing_company_or_point(
    as_company_owner: ApiClient,
    company_id: int,
    point_id: int,
    department_data: dict,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_id, "point_pk": point_id},
        ),
        department_data,
        expected_status=status.HTTP_404_NOT_FOUND,
    )

    assert_doesnt_exist(Department)


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"name": ""},
    ],
)
def test_create_department_invalid_data(
    as_company_owner: ApiClient,
    company_point: Point,
    invalid_data: dict,
    factory: FixtureFactory,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_point.company.id, "point_pk": company_point.id},
        ),
        data=factory.department_data(**invalid_data),
        expected_status=status.HTTP_400_BAD_REQUEST,
    )

    assert_doesnt_exist(Department)


def test_point_field_is_ignored_on_department_creation(
    as_company_owner: ApiClient,
    company_point: Point,
    department_data: dict,
    factory: FixtureFactory,
    assert_department: ModelAssertion,
):
    as_company_owner.post(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_point.company.id, "point_pk": company_point.id},
        ),
        department_data | {"point": factory.company_point().id},
        expected_status=status.HTTP_201_CREATED,
    )

    assert_department(department_data, point=company_point)


def test_department_list(
    reader_client: ApiClient,
    company_point: Point,
    factory: FixtureFactory,
    assert_rest_page: RestPageAssertion,
):
    departments = sorted(factory.cycle(5).department(point=company_point), key=lambda d: d.name)
    response = reader_client.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-list",
            kwargs={"company_pk": company_point.company.id, "point_pk": company_point.id},
        )
    )

    assert_rest_page(response, departments, DepartmentSerializer, None, None)


def test_department_retrieve(
    reader_client: ApiClient,
    department: Department,
):
    response = reader_client.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        )
    )

    assert response == DepartmentSerializer(department).data


def test_point_managing_staff_can_update_department(
    as_point_managing_staff: ApiClient,
    department: Department,
    department_data: dict,
    assert_department: ModelAssertion,
):
    response = as_point_managing_staff.patch(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        ),
        department_data,
    )
    department.refresh_from_db()

    assert_department(department_data, point=department.point)
    assert response == DepartmentSerializer(department).data


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"name": ""},
    ],
)
def test_company_owner_cannot_update_department_with_invalid_data(
    as_company_owner: ApiClient,
    department: Department,
    invalid_data: dict,
    factory: FixtureFactory,
    assert_department: ModelAssertion,
):
    department_data = DepartmentSerializer(department).data
    as_company_owner.patch(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        ),
        data=factory.department_data(**invalid_data),
        expected_status=status.HTTP_400_BAD_REQUEST,
    )

    assert_department(department_data, point=department.point)


@pytest.mark.parametrize(*non_point_managing_users_parametrization)
def test_non_point_managing_staff_cannot_update_department(
    client: ApiClient,
    status_code: int,
    message: str,
    department: Department,
    department_data: dict,
    assert_department: ModelAssertion,
):
    response = client.patch(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        ),
        department_data,
        expected_status=status_code,
    )

    assert_department(DepartmentSerializer(department).data, point=department.point)
    assert response == {"detail": message}


def test_point_managing_staff_can_delete_department(
    as_point_managing_staff: ApiClient,
    department: Department,
    assert_doesnt_exist: ExistCheckAssertion,
):
    as_point_managing_staff.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        )
    )

    assert_doesnt_exist(Department)


@pytest.mark.parametrize(*non_point_managing_users_parametrization)
def test_non_point_managing_staff_cannot_delete_department(
    client: ApiClient, status_code: int, message: str, department: Department
):
    response = client.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:companies:department-detail",
            kwargs={
                "company_pk": department.point.company.id,
                "point_pk": department.point.id,
                "pk": department.id,
            },
        ),
        expected_status=status_code,
    )

    assert Department.objects.filter(id=department.id).exists()
    assert response == {"detail": message}
