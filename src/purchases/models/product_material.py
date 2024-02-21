from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted, TimestampedModel
from purchases.models.managers import MaterialManager, MaterialQuerySet


class ProductMaterial(ArchiveDeleted, TimestampedModel):
    class Meta:
        verbose_name = _("product material")
        verbose_name_plural = _("product materials")
        ordering = ("price",)

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

    objects = MaterialManager()
    include_archived = MaterialQuerySet.as_manager()

    def __str__(self) -> str:
        return f"Product: {self.material.material.name}"

    def get_absolute_url(self) -> str:
        return reverse(
            "api_v1:purchases:product-detail",
            kwargs={
                "company_pk": self.material.stock.point.company.pk,
                "point_pk": self.material.stock.point.pk,
                "pk": self.pk,
            },
        )
