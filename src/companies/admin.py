from django.contrib import admin

from companies.models import Company, Point


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner")


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ("id", "company", "address")
