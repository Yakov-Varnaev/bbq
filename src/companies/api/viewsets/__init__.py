from companies.api.viewsets.company import CompanyViewSet
from companies.api.viewsets.department import CategoryViewSet, DepartmentViewSet, ProcedureViewSet
from companies.api.viewsets.employee import EmployeeViewSet, MasterProcedureViewSet
from companies.api.viewsets.point import ConsumableMaterialViewSet, PointViewSet
from companies.api.viewsets.stock import MaterialTypeViewSet, MaterialViewSet, StockMaterialViewSet, StockViewSet

__all__ = [
    "CategoryViewSet",
    "CompanyViewSet",
    "ConsumableMaterialViewSet",
    "PointViewSet",
    "DepartmentViewSet",
    "EmployeeViewSet",
    "MasterProcedureViewSet",
    "ProcedureViewSet",
    "StockViewSet",
    "StockMaterialViewSet",
    "MaterialTypeViewSet",
    "MaterialViewSet",
]
