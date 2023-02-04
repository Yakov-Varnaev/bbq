from django.contrib import admin
from .models import CompaniesModel


class CompaniesAdmin(admin.ModelAdmin):
    pass


admin.site.register(CompaniesModel, CompaniesAdmin)
