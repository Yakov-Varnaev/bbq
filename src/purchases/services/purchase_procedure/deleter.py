from django.db import transaction

from app.services import BaseService
from purchases.models import PurchaseProcedure


class PurchaseProcedureDeleter(BaseService):
    def __init__(self, purchase_procedure: PurchaseProcedure) -> None:
        self.purchase_procedure = purchase_procedure

    @transaction.atomic
    def act(self) -> None:
        self.purchase_procedure.used_materials.all().delete()
        self.purchase_procedure.delete()
