from django.contrib import admin

from .models import Company, CompanyPoint, Employee


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'time_created', 'time_updated']


@admin.register(CompanyPoint)
class CompanyPointAdmin(admin.ModelAdmin):
    list_display = ['id', 'address', 'get_name']

    @admin.display(ordering='company__address', description='Comapny Name')
    def get_name(self, obj):
        return obj.company.name


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'position', 'get_address']

    @admin.display(ordering='user__username', description='Username')
    def get_username(self, obj):
        return obj.user.username

    @admin.display(ordering='object__address', description='Address')
    def get_address(self, obj):
        return obj.point.address
