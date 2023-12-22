from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import DefaultModel


class MaterialType(DefaultModel):
    class Meta:
        verbose_name = _("material type")
        verbose_name_plural = _("material types")

    name = models.CharField(
        _("material type name"),
        max_length=255,
    )


class Material(DefaultModel):
    class Meta:
        verbose_name = _("material")
        verbose_name_plural = _("materials")

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


class StockMaterial(DefaultModel):
    class Meta:
        verbose_name = _("stock material")
        verbose_name_plural = _("stock materials")

    material = models.ForeignKey(
        "Material",
        on_delete=models.PROTECT,
        related_name="stock_materials",
    )
    price = models.DecimalField(
        _("material price"),
        max_digits=10,
        decimal_places=2,
    )
    quantity = models.IntegerField(
        _("material quantity"),
    )
    stock = models.ForeignKey(
        "Stock",
        on_delete=models.PROTECT,
        related_name="materials",
    )


class StockQuerySet(models.QuerySet):
    def with_material_count(self) -> "StockQuerySet":
        return self.annotate(material_count=models.Count("materials"))

    def with_order_sum(self) -> "StockQuerySet":
        return self.annotate(order_sum=models.Sum("materials__price", default=0))


class StockManager(models.Manager):
    def get_queryset(self) -> StockQuerySet:
        return StockQuerySet(self.model, using=self._db)

    def with_material_count(self) -> StockQuerySet:
        return self.get_queryset().with_material_count()

    def with_order_sum(self) -> StockQuerySet:
        return self.get_queryset().with_order_sum()

    def detailed(self) -> StockQuerySet:
        return self.with_material_count().with_order_sum()


class Stock(DefaultModel):
    objects = StockManager()

    class Meta:
        verbose_name = _("stock")
        verbose_name_plural = _("stocks")
        ordering = ["-date"]

    class Status(models.TextChoices):
        DRAFT = "draft", _("draft")
        INPROGRESS = "progress", _("progress")
        DONE = "done", _("done")
        CANCELED = "canceled", _("canceled")

    date = models.DateField(
        _("stock date"),
    )
    point = models.ForeignKey(
        "companies.Point",
        on_delete=models.PROTECT,
        related_name="stocks",
    )
    status = models.CharField(
        _("stock status"),
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
