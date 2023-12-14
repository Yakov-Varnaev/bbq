from django.contrib import admin

from companies.models import Company, Department, Employee, Point


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
