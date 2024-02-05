from decimal import Decimal
from typing import TypedDict

from companies.models.stock import StockMaterial


class ProductMaterialData(TypedDict, total=False):
    material: StockMaterial
    price: Decimal
