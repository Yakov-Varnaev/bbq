import pytest
from pytest import FixtureRequest  # noqa: PT013
from typing import Any

from pytest_lazyfixture import lazy_fixture as lf
from rest_framework import status

from django.contrib.auth import get_user_model

from app.testing import ApiClient, StatusApiClient
from app.types import GenericModelAssertion, ModelAssertion
from companies.models import (
    Category,
    Company,
    Department,
    Employee,
    MasterProcedure,
    MaterialType,
    Point,
    Procedure,
    StockMaterial,
)
from companies.types import (
    CategoryData,
    CompanyData,
    DepartmentData,
    EmployeeData,
    MasterProcedureData,
    PointData,
    ProcedureData,
)

User = get_user_model()


class CompanyAssert(GenericModelAssertion[CompanyData]):
    def __call__(self, data: CompanyData, **extra: Any) -> None:
        merged_data = data | extra
        company_id = merged_data["id"]
        assert isinstance(company_id, int)
        company = Company.objects.get(id=company_id)

        for key, value in merged_data.items():
            assert getattr(company, key) == value, f"{key} is not {value} but {getattr(company, key)}"


@pytest.fixture
def assert_company() -> GenericModelAssertion:
    return CompanyAssert()


class PointAssert(GenericModelAssertion[PointData]):
    def __call__(self, data: PointData, **extra: Any) -> None:
        merged_data = data | extra
        point_id = merged_data["id"]
        assert isinstance(point_id, int)
        point = Point.objects.get(id=point_id)

        for key, value in merged_data.items():
            assert getattr(point, key) == value, f"{key} is not {value} but {getattr(point, key)}"


@pytest.fixture
def assert_company_point() -> GenericModelAssertion:
    return PointAssert()


class DepartmentAssert(GenericModelAssertion[DepartmentData]):
    def __call__(self, data: DepartmentData, **extra: Any) -> None:
        merged_data = data | extra
        department_id = merged_data["id"]
        assert isinstance(department_id, int)
        department = Department.objects.get(id=department_id)

        for key, value in merged_data.items():
            assert getattr(department, key) == value, f"{key} is not {value} but {getattr(department, key)}"


@pytest.fixture
def assert_department() -> GenericModelAssertion:
    return DepartmentAssert()


class CategoryAssert(GenericModelAssertion[CategoryData]):
    def __call__(self, data: CategoryData, **extra: Any) -> None:
        merged_data = data | extra
        category_id = merged_data["id"]
        assert isinstance(category_id, int)
        category = Category.objects.get(id=category_id)

        for key, value in merged_data.items():
            assert getattr(category, key) == value, f"{key} is not {value} but {getattr(category, key)}"


@pytest.fixture
def assert_category() -> GenericModelAssertion:
    return CategoryAssert()


class ProcedureAssert(GenericModelAssertion[ProcedureData]):
    def __call__(self, data: ProcedureData, **extra: Any) -> None:
        merged_data = data | extra
        procedure_id = merged_data["id"]
        assert isinstance(procedure_id, int)
        procedure = Procedure.objects.get(id=procedure_id)

        for key, value in merged_data.items():
            assert getattr(procedure, key) == value, f"{key} is not {value} but {getattr(procedure, key)}"


@pytest.fixture
def assert_procedure() -> GenericModelAssertion:
    return ProcedureAssert()


class EmployeeAssert(GenericModelAssertion[EmployeeData]):
    def __call__(self, data: EmployeeData, **extra: Any) -> None:
        merged_data = data | extra
        employee_id = merged_data["id"]
        assert isinstance(employee_id, int)
        employee = Employee.objects.get(id=employee_id)
        assert sorted([d.id for d in employee.departments.all()]) == sorted(merged_data.pop("departments"))
        assert employee.user.id == merged_data.pop("user")

        for key, value in merged_data.items():
            assert getattr(employee, key) == value, f"{key} is not {value} but {getattr(employee, key)}"


@pytest.fixture
def assert_employee() -> GenericModelAssertion:
    return EmployeeAssert()


class MasterProcedureAssert(GenericModelAssertion[MasterProcedureData]):
    def __call__(self, data: MasterProcedureData, **extra: Any) -> None:
        merged_data = data | extra
        master_procedure_id = merged_data["id"]
        assert isinstance(master_procedure_id, int)
        master_procedure = MasterProcedure.objects.get(id=master_procedure_id)
        assert master_procedure.procedure.id == data.pop("procedure")
        assert master_procedure.employee.id == data.pop("employee")

        for key, value in merged_data.items():
            assert getattr(master_procedure, key) == value, f"{key} is not {value} but {getattr(master_procedure, key)}"


@pytest.fixture
def assert_master_procedure() -> GenericModelAssertion:
    return MasterProcedureAssert()


@pytest.fixture
def assert_material_type() -> ModelAssertion:
    def _assert_material_type(data: dict, **extra: Any) -> None:
        material_type = MaterialType.objects.get(name=data["name"])
        for field_name, expected_value in (data | extra).items():
            assert getattr(material_type, field_name) == expected_value

    return _assert_material_type


@pytest.fixture
def assert_stock_material() -> ModelAssertion:
    def _assert_stock_material(data: dict, **extra: Any) -> None:
        stock_material = StockMaterial.objects.get(material_id=data["material"])
        assert stock_material.material.id == data.pop("material")

        for field_name, expected_value in (data | extra).items():
            assert getattr(stock_material, field_name) == expected_value

    return _assert_stock_material


@pytest.fixture(
    params=[
        lf("as_anon"),
        lf("as_user"),
        lf("as_company_owner"),
        lf("as_another_company_owner"),
    ],
)
def reader_client(request) -> ApiClient:
    return request.param


@pytest.fixture(
    params=[
        lf("as_company_owner"),
    ]
)
def as_point_managing_staff(request) -> ApiClient:
    return request.param


@pytest.fixture
def user_fixtures_collection(
    as_another_company_owner: ApiClient, as_user: ApiClient, as_anon: ApiClient
) -> dict[str, ApiClient]:
    return {
        "as_another_company_owner": as_another_company_owner,
        "as_user": as_user,
        "as_anon": as_anon,
    }


@pytest.fixture(
    params=[
        ("as_another_company_owner", status.HTTP_403_FORBIDDEN),
        ("as_user", status.HTTP_403_FORBIDDEN),
        ("as_anon", status.HTTP_401_UNAUTHORIZED),
    ]
)
def as_point_non_managing_staff(
    request: FixtureRequest, user_fixtures_collection: dict[str, ApiClient]
) -> StatusApiClient:
    user, status = request.param
    client: ApiClient = user_fixtures_collection[user]
    return StatusApiClient(status, getattr(client, "user", None))
