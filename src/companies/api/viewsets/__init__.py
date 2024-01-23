from companies.api.viewsets.company import CompanyViewSet
from companies.api.viewsets.department import DepartmentViewSet, ProcedureViewSet
from companies.api.viewsets.employee import EmployeeViewSet
from companies.api.viewsets.point import PointViewSet
from companies.api.viewsets.stock import MaterialTypeViewSet, MaterialViewSet, StockMaterialViewSet, StockViewSet

__all__ = [
    "CompanyViewSet",
    "PointViewSet",
    "DepartmentViewSet",
    "EmployeeViewSet",
    "ProcedureViewSet",
    "StockViewSet",
    "StockMaterialViewSet",
    "MaterialTypeViewSet",
    "MaterialViewSet",
]
