from django.contrib import admin

from companies.models import Company, Department, Employee, Material, MaterialType, Point, Stock, StockMaterial


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "address")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "point", "name")

    def company(self, department: Department) -> Company:
        return department.point.company


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "position", "fire_date")

    def user(self, employee: Employee) -> str:
        return str(employee.user)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "point", "date", "status")

    def point(self, stock: Stock) -> Point:
        return stock.point


@admin.register(StockMaterial)
class StockMaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "stock", "material", "quantity", "price")

    def stock(self, stock_material: StockMaterial) -> Stock:
        return stock_material.stock

    def material(self, stock_material: StockMaterial) -> Material:
        return stock_material.material


@admin.register(MaterialType)
class MaterialTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("id", "brand", "name", "unit", "kind")
