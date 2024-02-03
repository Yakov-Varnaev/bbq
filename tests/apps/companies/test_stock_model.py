import pytest

from django.utils import timezone

from app.testing.factory import FixtureFactory
from companies.models import Stock

pytestmark = pytest.mark.django_db


def test_stock_is_created_with_draft_status(factory: FixtureFactory):
    stock = Stock.objects.create(date=timezone.now(), point=factory.company_point())
    assert stock.status == Stock.Status.DRAFT


def test_stock_with_materials_count_query(stock):
    stocks = Stock.objects.with_material_count()

    assert stocks[0].material_count == 0


def test_stock_with_order_sum_query(stock):
    stocks = Stock.objects.with_order_sum()

    assert stocks[0].order_sum == 0


def test_stock_detailed_query(stock):
    stocks = Stock.objects.detailed()

    assert stocks[0].material_count == 0
    assert stocks[0].order_sum == 0
