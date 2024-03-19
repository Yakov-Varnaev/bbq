from django_filters import rest_framework as filters
from rest_framework.exceptions import ValidationError

from django import forms
from django.db.models import QuerySet

from companies.models import Company


class CompanyFilterSet(filters.FilterSet):
    user = filters.NumberFilter(field_name="user", method="filter_user")

    def filter_user(self, queryset: QuerySet[Company], _: str, value: int) -> QuerySet[Company]:
        return queryset.filter(owner_id=value)


class MaterialDataFilterForm(forms.Form):
    date_from = forms.DateField()
    date_to = forms.DateField()

    def is_valid(self, query_params: dict | None = None) -> bool:
        valide = super().is_valid()
        if query_params and not valide:
            raise ValidationError(self.errors)  # type: ignore[arg-type]
        return valide
