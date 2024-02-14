from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedCreatedModel


class Purchase(TimestampedCreatedModel):
    is_paid_by_card = models.BooleanField(_("paid by card"))

    class Meta:
        verbose_name = _("purchase")
        verbose_name_plural = _("purchases")
        ordering = ("created",)
