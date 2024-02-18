from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import ArchiveDeleted


class PurchaseProcedure(ArchiveDeleted):
    purchase = models.ForeignKey(
        "purchases.Purchase",
        on_delete=models.PROTECT,
        related_name="purchase_procedures",
    )
    procedure = models.ForeignKey(
        "companies.Procedure",
        on_delete=models.PROTECT,
        related_name="purchase_procedures",
    )

    class Meta:
        verbose_name = _("purchase of procedure")
        verbose_name_plural = _("purchase of procedures")
        ordering = ("purchase", "procedure")
