from datetime import datetime
from decimal import Decimal
from typing import TypedDict

from companies.models import Procedure, StockMaterial
from purchases.models import Purchase


class ProductMaterialData(TypedDict, total=False):
    material: StockMaterial
    price: Decimal


class PurchaseData(TypedDict, total=False):
    created: datetime
    is_paid_by_card: bool


class PurchaseProcedureData(TypedDict, total=False):
    procedure: Procedure
    purchase: Purchase
