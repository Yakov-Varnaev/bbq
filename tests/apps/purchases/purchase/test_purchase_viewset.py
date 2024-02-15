import pytest

from django.urls import reverse
from django.utils import timezone

from app.testing.api import ApiClient, StatusApiClient
from app.testing.factory import FixtureFactory
from app.types import GenericExistCheckAssertion, GenericModelAssertion, RestPageAssertion
from companies.models import Procedure
from purchases.api.serializers import PurchaseSerializer
from purchases.models import Purchase, PurchaseProcedure
from purchases.types import PurchaseData

pytestmark = pytest.mark.django_db


@pytest.mark.freeze_time("2022-01-01")
def test_point_managing_staff_can_create_purchase(
    as_point_managing_staff: ApiClient,
    purchase_data: PurchaseData,
    procedure: Procedure,
    assert_purchase: GenericModelAssertion[PurchaseData],
):
    url = reverse(
        "api_v1:purchases:purchase-list",
        kwargs={
            "company_pk": procedure.department.point.company.pk,
            "point_pk": procedure.department.point.pk,
        },
    )
    response = as_point_managing_staff.post(url, data=purchase_data)  # type: ignore[no-untyped-call]

    assert_purchase(
        purchase_data,
        id=response["id"],
        created=timezone.now(),
    )


def test_non_point_managing_staff_cannot_create_purchase(
    as_point_non_managing_staff: StatusApiClient,
    purchase_data: PurchaseData,
    procedure: Procedure,
    assert_doesnt_exist: GenericExistCheckAssertion[type[Purchase]],
):
    url = reverse(
        "api_v1:purchases:purchase-list",
        kwargs={
            "company_pk": procedure.department.point.company.pk,
            "point_pk": procedure.department.point.pk,
        },
    )
    as_point_non_managing_staff.post(  # type: ignore[no-untyped-call]
        url,
        data=purchase_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_doesnt_exist(Purchase)


def test_point_managing_staff_has_access_to_retrieve(
    as_point_managing_staff: ApiClient,
    purchase_procedure: PurchaseProcedure,
):
    response = as_point_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": purchase_procedure.procedure.department.point.company.pk,
                "point_pk": purchase_procedure.procedure.department.point.pk,
                "pk": purchase_procedure.purchase.pk,
            },
        )
    )

    assert response == PurchaseSerializer(purchase_procedure.purchase).data


def test_point_managing_staff_has_no_access_to_retrieve(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure: PurchaseProcedure,
):
    as_point_non_managing_staff.get(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": purchase_procedure.procedure.department.point.company.pk,
                "point_pk": purchase_procedure.procedure.department.point.pk,
                "pk": purchase_procedure.purchase.pk,
            },
        ),
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
            "api_v1:purchases:purchase-list",
            kwargs={
                "company_pk": purchase_procedures[0].procedure.department.point.company.pk,
                "point_pk": purchase_procedures[0].procedure.department.point.pk,
            },
        )
    )
    purchases = Purchase.objects.point(
        purchase_procedures[0].procedure.department.point.company.pk,
        purchase_procedures[0].procedure.department.point.pk,
    ).all()

    assert_rest_page(response, purchases, PurchaseSerializer)


@pytest.mark.freeze_time("2022-01-01")
def test_point_managing_staff_can_update_purchase(
    as_point_managing_staff: ApiClient,
    factory: FixtureFactory,
    purchase: Purchase,
    procedure: Procedure,
    purchase_data: PurchaseData,
    assert_purchase: GenericModelAssertion[PurchaseData],
):
    purchase_procedure = factory.purchase_procedure(purchase=purchase, procedure=procedure)
    as_point_managing_staff.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": purchase_procedure.procedure.department.point.company.pk,
                "point_pk": purchase_procedure.procedure.department.point.pk,
                "pk": purchase_procedure.purchase.pk,
            },
        ),
        data=purchase_data,
    )
    purchase.refresh_from_db()

    assert_purchase(
        purchase_data,
        id=purchase.id,
        created=timezone.now(),
    )


@pytest.mark.freeze_time("2022-01-01")
def test_point_non_managing_staff_cannot_update_purchase(
    as_point_non_managing_staff: StatusApiClient,
    factory: FixtureFactory,
    purchase: Purchase,
    procedure: Procedure,
    purchase_data: PurchaseData,
    assert_purchase: GenericModelAssertion[PurchaseData],
):
    purchase_procedure = factory.purchase_procedure(purchase=purchase, procedure=procedure)
    as_point_non_managing_staff.put(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": purchase_procedure.procedure.department.point.company.pk,
                "point_pk": purchase_procedure.procedure.department.point.pk,
                "pk": purchase_procedure.purchase.pk,
            },
        ),
        data=purchase_data,
        expected_status=as_point_non_managing_staff.expected_status,
    )
    purchase.refresh_from_db()

    assert_purchase(
        {},
        is_paid_by_card=purchase.is_paid_by_card,
        id=purchase.id,
        created=timezone.now(),
    )


@pytest.mark.skip("not implemented")
def test_deletion_by_as_point_managing_staff_leads_to_archiving():
    ...


def test_point_non_managing_staff_cannot_delete_purchase(
    as_point_non_managing_staff: StatusApiClient,
    purchase_procedure: PurchaseProcedure,
    assert_purchase: GenericModelAssertion[PurchaseData],
):
    as_point_non_managing_staff.delete(  # type: ignore[no-untyped-call]
        reverse(
            "api_v1:purchases:purchase-detail",
            kwargs={
                "company_pk": purchase_procedure.procedure.department.point.company.pk,
                "point_pk": purchase_procedure.procedure.department.point.pk,
                "pk": purchase_procedure.purchase.pk,
            },
        ),
        expected_status=as_point_non_managing_staff.expected_status,
    )

    assert_purchase(
        {},
        is_paid_by_card=purchase_procedure.purchase.is_paid_by_card,
        id=purchase_procedure.purchase.id,
        created=purchase_procedure.purchase.created,
    )
