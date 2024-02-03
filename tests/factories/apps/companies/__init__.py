from tests.factories.apps.companies.company import company, company_data
from tests.factories.apps.companies.department import category, department, department_data, procedure, procedure_data
from tests.factories.apps.companies.employee import employee, employee_data, master_procedure, master_procedure_data
from tests.factories.apps.companies.point import company_point, company_point_data
from tests.factories.apps.companies.stock import (
    material,
    material_type,
    material_type_data,
    stock,
    stock_data,
    stock_material,
    stock_material_data,
)

__all__ = [
    "company",
    "company_data",
    "category",
    "department",
    "department_data",
    "procedure",
    "procedure_data",
    "employee",
    "employee_data",
    "master_procedure",
    "master_procedure_data",
    "company_point",
    "company_point_data",
    "material",
    "material_type",
    "material_type_data",
    "stock",
    "stock_data",
    "stock_material",
    "stock_material_data",
]
