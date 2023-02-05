from django.contrib import admin

from .models import CompaniesModel


@admin.register(CompaniesModel)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'time_created', 'time_updated']

