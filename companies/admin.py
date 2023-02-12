from django.contrib import admin

from .models import Company


@admin.register(Company)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'time_created', 'time_updated']

