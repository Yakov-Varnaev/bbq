from typing import Self

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import DefaultModel, StoreDeleted, StoreDeletedManager, StoreDeletedQuerySet


class ProductMaterialQuerySet(StoreDeletedQuerySet):
    def with_material_info(self) -> Self:
        return self.annotate(
            name=models.F("material__material__name"),
            brand=models.F("material__material__brand"),
            kind=models.F("material__material__kind"),
            unit=models.F("material__material__unit"),
        )

    def point(self, company_id: int, point_id: int) -> Self:
        return self.filter(
            material__stock__point__company_id=company_id,
            material__stock__point_id=point_id,
        )


class ProductMaterialManager(StoreDeletedManager):
    def get_queryset(self) -> ProductMaterialQuerySet:
        return ProductMaterialQuerySet(self.model, using=self._db).not_deleted()

    def with_material_info(self) -> ProductMaterialQuerySet:
        return self.get_queryset().with_material_info()

    def point(self, company_id: int, point_id: int) -> ProductMaterialQuerySet:
        return self.get_queryset().point(company_id, point_id)


class ProductMaterial(StoreDeleted, DefaultModel):
    class Meta:
        verbose_name = _("product material")
        verbose_name_plural = _("product materials")

    material = models.ForeignKey(
        "companies.StockMaterial",
        on_delete=models.PROTECT,
        related_name="product_materials",
    )
    price = models.DecimalField(
        _("price"),
        max_digits=10,
        decimal_places=2,
    )

    objects = ProductMaterialManager()
    allow_deleted = ProductMaterialQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Product: {self.material.material.name}"
