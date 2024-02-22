import pytest

from rest_framework import status

from django.urls import reverse

from app.testing.api import ApiClient, StatusApiClient
from app.testing.factory import FixtureFactory
from app.types import GenericExistCheckAssertion, GenericModelAssertion, RestPageAssertion
from companies.models import Procedure
from purchases.api.serializers import PurchaseProcedureReadSerializer
from purchases.models import Purchase, PurchaseProcedure, UsedMaterial
from purchases.types import PurchaseProcedureData, UsedMaterialData

pytestmark = pytest.mark.django_db


def test_point_managing_staff_can_create_purchase_procedure(
    as_point_managing_staff: ApiClient,
    purchase_procedure_data: PurchaseProcedureData,
    used_materials_data_without_procedure: list[UsedMaterialData],
    procedure: Procedure,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
    assert_used_material: GenericModelAssertion[UsedMaterialData],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure
    url = reverse(
        "api_v1:purchases:procedures-purchase-list",
        kwargs={
            "company_pk": procedure.department.point.company.pk,
            "point_pk": procedure.department.point.pk,
        },
    )
    response = as_point_managing_staff.post(url, data=purchase_procedure_data)  # type: ignore[no-untyped-call]

    assert_purchase_procedure(purchase_procedure_data, id=response["id"])
    purchase_procedure = PurchaseProcedure.objects.get(id=response["id"])
    used_materials = sorted(purchase_procedure.used_materials.all(), key=lambda x: x.material.id)
    for used_material, material_data in zip(used_materials, used_materials_data_without_procedure):
        assert_used_material(material_data, procedure=purchase_procedure, id=used_material.id)


def test_point_managing_staff_cannot_create_purchase_not_unique_materials(
    as_point_managing_staff: ApiClient,
    purchase_procedure_data: PurchaseProcedureData,
    used_materials_data_without_procedure_and_not_unique: list[UsedMaterialData],
    procedure: Procedure,
    assert_doesnt_exist: GenericExistCheckAssertion[type[PurchaseProcedure | UsedMaterial]],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure_and_not_unique
    url = reverse(
        "api_v1:purchases:procedures-purchase-list",
        kwargs={
            "company_pk": procedure.department.point.company.pk,
            "point_pk": procedure.department.point.pk,
        },
    )
    as_point_managing_staff.post(url, data=purchase_procedure_data, expected_status=status.HTTP_400_BAD_REQUEST)  # type: ignore[no-untyped-call]

    assert_doesnt_exist(PurchaseProcedure)
    assert_doesnt_exist(UsedMaterial)


def test_non_point_managing_staff_cannot_create_purchase_procedure(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure_data: PurchaseProcedureData,
    used_materials_data_without_procedure: list[UsedMaterialData],
    procedure: Procedure,
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure
    url = reverse(
        "api_v1:purchases:procedures-purchase-list",
        kwargs={
            "company_pk": procedure.department.point.company.pk,
            "point_pk": procedure.department.point.pk,
        },
    )
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        url,
        data=purchase_procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_non_managing_staff_has_no_access_to_retrieve(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure: PurchaseProcedure,
):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        purchase_procedure.get_absolute_url(),
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_managing_staff_has_access_to_list(
    as_point_managing_staff: ApiClient,
    factory: FixtureFactory,
    assert_rest_page: RestPageAssertion,
    purchase: Purchase,
    procedure: Procedure,
):
    purchase_procedures = factory.cycle(5).purchase_procedure(purchase=purchase, procedure=procedure)
    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:procedures-purchase-list",
            kwargs={
                "company_pk": purchase_procedures[0].procedure.department.point.company.pk,
                "point_pk": purchase_procedures[0].procedure.department.point.pk,
            },
        )
    )
    purchases = PurchaseProcedure.objects.point(
        purchase_procedures[0].procedure.department.point.company.pk,
        purchase_procedures[0].procedure.department.point.pk,
    )

    assert_rest_page(response, purchases, PurchaseProcedureReadSerializer)


def test_point_non_managing_staff_has_no_access_to_list(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure: PurchaseProcedure,
):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        purchase_procedure.get_absolute_url(),
        expected_status=as_point_non_managing_staff.expected_status,
    )


def test_point_managing_staff_can_update_purchase_procedure(
    as_point_managing_staff: ApiClient,
    purchase_procedure_with_one_material: PurchaseProcedure,
    purchase_procedure_data: PurchaseProcedureData,
    used_materials_data_without_procedure: list[UsedMaterialData],
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure
    as_point_managing_staff.put(  # type: ignore[no-untyped-call]
        purchase_procedure_with_one_material.get_absolute_url(),
        data=purchase_procedure_data,
    )
    purchase_procedure_with_one_material.refresh_from_db()

    assert_purchase_procedure(
        purchase_procedure_data,
        id=purchase_procedure_with_one_material.id,
        procedure=purchase_procedure_with_one_material.procedure.id,
    )


def test_point_managing_staff_cannot_update_purchase_procedure_not_unique_materials(
    as_point_managing_staff: ApiClient,
    purchase_procedure_with_one_material: PurchaseProcedure,
    purchase_procedure_data: PurchaseProcedureData,
    used_materials_data_without_procedure_and_not_unique: list[UsedMaterialData],
):
    purchase_procedure_data["materials"] = used_materials_data_without_procedure_and_not_unique
    as_point_managing_staff.put(  # type: ignore[no-untyped-call]
        purchase_procedure_with_one_material.get_absolute_url(),
        data=purchase_procedure_data,
        expected_status=status.HTTP_400_BAD_REQUEST,
    )


def test_point_non_managing_staff_cannot_update_purchase_procedure(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure: PurchaseProcedure,
    purchase_procedure_data: PurchaseProcedureData,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
):
    as_point_non_managing_staff.patch(  # type: ignore[no-untyped-call]
        purchase_procedure.get_absolute_url(),
        data=purchase_procedure_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_purchase_procedure(
        {},
        id=purchase_procedure.id,
        procedure=purchase_procedure.procedure.id,
        purchase=purchase_procedure.purchase.id,
    )


@pytest.mark.skip("not implemented")
def test_deletion_by_as_point_managing_staff_leads_to_archiving():
    ...


def test_point_non_managing_staff_cannot_delete_purchase(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure_with_one_material: PurchaseProcedure,
    assert_purchase_procedure: GenericModelAssertion[PurchaseProcedureData],
    assert_used_material: GenericModelAssertion[UsedMaterialData],
):
    as_point_non_managing_staff.delete(  # type: ignore[no-untyped-call]
        purchase_procedure_with_one_material.get_absolute_url(),
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_purchase_procedure(
        {},
        id=purchase_procedure_with_one_material.id,
        procedure=purchase_procedure_with_one_material.procedure.id,
        purchase=purchase_procedure_with_one_material.purchase.id,
    )
    used_materials = sorted(purchase_procedure_with_one_material.used_materials.all(), key=lambda x: x.material.id)
    for used_material in used_materials:
        assert_used_material(
            {},
            material=used_material.material.id,
            amount=used_material.amount,
            procedure=purchase_procedure_with_one_material,
            id=used_material.id,
        )
