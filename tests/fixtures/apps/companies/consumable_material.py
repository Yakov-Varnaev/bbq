import pytest
from datetime import datetime, timedelta

from freezegun import freeze_time

from app.testing.factory import FixtureFactory
from companies.models import Point, Procedure


@pytest.fixture
def material_date_query_params() -> dict[str, str]:
    return {"date_from": "2000-01-01", "date_to": str(datetime.now().date())}


@pytest.fixture
@freeze_time("2020-01-01")
def point_with_consumable_materials(factory: FixtureFactory, procedure: Procedure) -> Point:
    modified = datetime.strptime("2000-01-01", "%Y-%m-%d")
    point = procedure.department.point
    stock_material = factory.stock_material(
        stock=factory.stock(point=point, date=modified),
    )
    for date in [modified + timedelta(days=200 * i) for i in range(1, 20)]:
        stock_material = factory.stock_material(
            stock=factory.stock(point=point, date=date),
        )
        factory.used_material(
            procedure=factory.purchase_procedure(procedure=procedure),
            material=stock_material,
        )
    return point
