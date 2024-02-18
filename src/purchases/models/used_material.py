from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted, TimestampedModel
from purchases.models.managers import _MaterialManager, _MaterialQuerySet


class UsedMaterial(ArchiveDeleted, TimestampedModel):
    procedure = models.ForeignKey(
        "purchases.PurchaseProcedure",
        on_delete=models.PROTECT,
        related_name="used_materials",
    )
    material = models.ForeignKey(
        "companies.StockMaterial",
        on_delete=models.PROTECT,
        related_name="used_materials",
    )
    amount = models.PositiveIntegerField(_("amount"))

    objects = _MaterialManager()
    include_archived = _MaterialQuerySet.as_manager()

    class Meta:
        verbose_name = _("used material")
        verbose_name_plural = _("used materials")
        ordering = ("material", "procedure")

    def __str__(self) -> str:
        return f"The material {self.material.material.name} used in the amount of: {self.amount}."
