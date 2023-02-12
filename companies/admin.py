from django.contrib import admin

from .models import CompanyModel


@admin.register(CompanyModel)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'time_created', 'time_updated']

