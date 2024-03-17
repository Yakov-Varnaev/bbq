from django.contrib.postgres.expressions import ArraySubquery  # type:ignore[import-untyped]
from django.db import models
from django.db.models import F, OuterRef, QuerySet, Sum
from django.db.models.functions import JSONObject, TruncDate
from django.utils.translation import gettext_lazy as _

from app.models import DefaultModel
from companies.models.stock import StockMaterial
from purchases.models import UsedMaterial


class MaterialType(DefaultModel):
    name = models.CharField(
        _("material type name"),
        max_length=255,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = _("material type")
        verbose_name_plural = _("material types")


class MaterialQuerySet(QuerySet):
    def point(self, company_id: int, point_id: int) -> "MaterialQuerySet":
        stock_queryset = StockMaterial.objects.prefetch_related("material", "stock").filter(
            stock__point__company__id=company_id,
            stock__point__id=point_id,
        )
        stocks = (
            stock_queryset.filter(material=OuterRef("id"))
            .order_by("stock__date")
            .values("material_id", date=F("stock__date"))
            .annotate(amount=Sum("quantity"))
            .annotate(  # noqa: BLK100
                stocks=JSONObject(
                    data=F("date"),
                    amount=F("amount")
                )
            )
            .values_list("stocks", flat=True)
        )
        usage_queryset = UsedMaterial.objects.with_material_info().point(company_id, point_id)
        usage = (
            usage_queryset.filter(material=OuterRef("id"))
            .annotate(date=TruncDate("modified"))
            .order_by("date")
            .values("material", "date")
            .annotate(amount=Sum("amount"))
            .annotate(
                stocks=JSONObject(
                    data=F("date"),
                    amount=F("amount")
                )
            )
            .values_list("stocks", flat=True)
        )
        material_ids = set(
            list(
                stock_queryset.values_list("material_id", flat=True)
            ) + list(
                usage_queryset.values_list("material_id", flat=True)
            )
        )
        return self.filter(id__in=material_ids).annotate(
            stocks=ArraySubquery(stocks), usage=ArraySubquery(usage)
        )


class Material(DefaultModel):
    brand = models.CharField(
        _("material brand"),
        max_length=255,
    )
    name = models.CharField(
        _("material name"),
        max_length=255,
    )
    unit = models.CharField(
        _("material unit"),
        max_length=255,
    )
    kind = models.ForeignKey(
        "MaterialType",
        on_delete=models.PROTECT,
        related_name="materials",
    )

    objects = MaterialQuerySet.as_manager()

    class Meta:
        ordering = ("name",)
        verbose_name = _("material")
        verbose_name_plural = _("materials")
