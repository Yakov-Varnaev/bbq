from behaviors.behaviors import StoreDeleted

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import DefaultModel, StoreDeletedQuerySet


class ProductMaterialQuerySet(StoreDeletedQuerySet):
    def with_material_info(self):
        return self.annotate(
            name=models.F("material__material__name"),
            brand=models.F("material__material__brand"),
            type=models.F("material__material__type"),
            unit=models.F("material__material__unit"),
        )

    def point(self, company_id: int, point_id: int):
        return self.filter(
            material__stock__point__company_id=company_id,
            material__stock__point_id=point_id,
        )

    def get_queryset(self):
        return self.not_deleted().with_material_info()


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

    objects = ProductMaterialQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Product: {self.material.material.name}"
