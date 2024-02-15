from typing import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from purchases.models import Purchase
from purchases.types import PurchaseData


@register
def purchase_data(self: FixtureFactory, **kwargs: Unpack[PurchaseData]) -> PurchaseData:
    schema = self.schema(
        schema=lambda: {
            "created": self.field("date"),
            "is_paid_by_card": self.field("boolean"),
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}  # type: ignore[typeddict-item]


@register
def purchase(self: FixtureFactory, **kwargs: Unpack[PurchaseData]) -> Purchase:
    return self.mixer.blend(Purchase, **kwargs)
