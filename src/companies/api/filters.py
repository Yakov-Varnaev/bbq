from django_filters import rest_framework as filters

from django.db.models import QuerySet

from companies.models import Company, Material


class CompanyFilterSet(filters.FilterSet):
    user = filters.NumberFilter(field_name="user", method="filter_user")

    def filter_user(self, queryset: QuerySet, _: str, value: int) -> QuerySet[Company]:
        return queryset.filter(owner_id=value)


class MaterialDataFilterSet(filters.FilterSet):
    date_from = filters.DateFilter()
    date_to = filters.DateFilter()

    def filter_queryset(self, queryset: QuerySet[Material]) -> QuerySet[Material]:
        return queryset
