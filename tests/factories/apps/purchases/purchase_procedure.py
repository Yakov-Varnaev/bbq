from typing import Unpack

from app.testing import register
from app.testing.factory import FixtureFactory
from purchases.models import PurchaseProcedure
from purchases.types import PurchaseProcedureData


@register
def purchase_procedure_data(self: FixtureFactory, **kwargs: Unpack[PurchaseProcedureData]) -> PurchaseProcedureData:
    procedure = kwargs.pop("procedure", None)
    if procedure is None:
        procedure = self.procedure()
    purchase = kwargs.pop("purchase", None)
    if purchase is None:
        purchase = self.purchase()
    schema = self.schema(
        schema=lambda: {
            "procedure": procedure.id,
            "purchase": purchase.id,
        },
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}  # type: ignore[typeddict-item]


@register
def purchase_procedure(self: FixtureFactory, **kwargs: Unpack[PurchaseProcedureData]) -> PurchaseProcedure:
    return self.mixer.blend(PurchaseProcedure, **kwargs)
