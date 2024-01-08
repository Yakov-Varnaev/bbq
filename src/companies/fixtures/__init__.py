from companies.fixtures.company import (
    another_company,
    another_company_owner,
    as_another_company_owner,
    as_company_owner,
    company,
    company_data,
    company_owner,
    company_pk,
)
from companies.fixtures.department import department, department_data, department_pk
from companies.fixtures.employee import (
    employee_data,
    employee_data_with_one_department,
    employee_data_with_several_departments,
    employee_invalid_data,
    employee_with_duplicating_department,
    employee_with_non_existing_department,
    employee_with_non_existing_user,
)
from companies.fixtures.point import company_point, company_point_data, company_point_pk
from companies.fixtures.stock import material, material_type, material_type_data, stock, stock_data, stock_material

__all__ = [
    "another_company",
    "another_company_owner",
    "as_another_company_owner",
    "as_company_owner",
    "company",
    "company_data",
    "company_owner",
    "company_pk",
    "company_point",
    "company_point_data",
    "company_point_pk",
    "department",
    "department_data",
    "department_pk",
    "employee_data",
    "employee_data_with_one_department",
    "employee_data_with_several_departments",
    "employee_invalid_data",
    "employee_with_duplicating_department",
    "employee_with_non_existing_department",
    "employee_with_non_existing_user",
    "material",
    "material_type",
    "material_type_data",
    "stock",
    "stock_data",
    "stock_material",
]
