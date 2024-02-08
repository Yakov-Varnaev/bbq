from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from companies.models import Category, Company, Department, Employee, Material, Point, Procedure, Stock
from users.models import User


class CompanyData(TypedDict, total=False):
    owner: User
    name: str
    created: datetime
    modified: datetime


class PointData(TypedDict, total=False):
    company: Company
    address: str
    created: datetime
    modified: datetime


class DepartmentData(TypedDict, total=False):
    point: Point
    name: str


class CategoryData(TypedDict, total=False):
    name: str


class ProcedureData(TypedDict, total=False):
    name: str
    category: Category
    department: Department


class EmployeeData(TypedDict, total=False):
    departments: list[Department]
    user: User
    position: str
    fire_date: datetime
    created: datetime
    modified: datetime


class MasterProcedureData(TypedDict, total=False):
    procedure: Procedure
    employee: Employee
    price: Decimal
    coef: float
    created: datetime
    modified: datetime
    archived: datetime


class MaterialTypeData(TypedDict, total=False):
    name: str


class StockMaterialTypeData(TypedDict, total=False):
    material: Material
    price: Decimal
    quantity: int
    stock: Stock
