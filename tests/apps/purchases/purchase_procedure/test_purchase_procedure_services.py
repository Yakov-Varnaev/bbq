import pytest

from app.types import GenericExistCheckAssertion, GenericModelAssertion
from purchases.api.serializers import PurchaseProcedureWriteSerializer
from purchases.models import PurchaseProcedure, UsedMaterial
from purchases.services.purchase_procedure import (
    PurchaseProcedureCreator,
    PurchaseProcedureDeleter,
    PurchaseProcedureUpdater,
)
from purchases.types import PurchaseProcedureData, UsedMaterialData

pytestmark = [pytest.mark.django_db]


def test_purchase_procedure_created_with_valid_data(
    used_materials_data_without_procedure: list[UsedMaterialData],
    purchase_procedure_data: PurchaseProcedureData,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
    assert_used_material: GenericModelAssertion[UsedMaterialData],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure
    purchase_procedure = PurchaseProcedureCreator(PurchaseProcedureWriteSerializer(data=purchase_procedure_data))()

    assert_purchase_procedure(purchase_procedure_data, id=purchase_procedure.id)
    used_materials = sorted(purchase_procedure.used_materials.all(), key=lambda x: x.material.id)
    for used_material, material_data in zip(used_materials, used_materials_data_without_procedure):
        assert_used_material(material_data, procedure=purchase_procedure, id=used_material.id)


def test_put_purchase_procedure_updated_with_valid_data(
    used_materials_data_without_procedure: list[UsedMaterialData],
    purchase_procedure: PurchaseProcedure,
    purchase_procedure_data: PurchaseProcedureData,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
    assert_used_material: GenericModelAssertion[UsedMaterialData],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure
    new_purchase_procedure = PurchaseProcedureUpdater(
        PurchaseProcedureWriteSerializer(data=purchase_procedure_data),
        purchase_procedure.id,
    )()

    assert_purchase_procedure(purchase_procedure_data, id=purchase_procedure.id)
    used_materials = sorted(new_purchase_procedure.used_materials.all(), key=lambda x: x.material.id)
    for used_material, material_data in zip(used_materials, used_materials_data_without_procedure):
        assert_used_material(material_data, procedure=new_purchase_procedure, id=used_material.id)


def test_patch_purchase_procedure_updated_with_valid_data(
    used_materials_data_without_procedure: list[UsedMaterialData],
    purchase_procedure_with_one_material: PurchaseProcedure,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
    assert_used_material: GenericModelAssertion[UsedMaterialData],
):
    data = {"materials": used_materials_data_without_procedure}
    serializer = PurchaseProcedureWriteSerializer(data=data, partial=True)
    PurchaseProcedureUpdater(serializer, purchase_procedure_with_one_material.id)()

    assert_purchase_procedure(
        {},
        id=purchase_procedure_with_one_material.id,
        procedure=purchase_procedure_with_one_material.procedure.id,
        purchase=purchase_procedure_with_one_material.purchase.id,
    )
    used_materials = sorted(purchase_procedure_with_one_material.used_materials.all(), key=lambda x: x.material.id)
    for used_material, material_data in zip(used_materials, data["materials"]):
        assert_used_material(material_data, procedure=purchase_procedure_with_one_material, id=used_material.id)


def test_purchase_procedure_deleted_with_valid_data(
    purchase_procedure_with_one_material: PurchaseProcedure,
    assert_doesnt_exist: GenericExistCheckAssertion,
):
    PurchaseProcedureDeleter(purchase_procedure_with_one_material)()

    assert_doesnt_exist(PurchaseProcedure)
    assert_doesnt_exist(UsedMaterial)
