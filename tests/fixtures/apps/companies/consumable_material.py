import pytest
from datetime import timedelta

from freezegun import freeze_time

from django.utils import timezone

from app.testing import FixtureFactory
from companies.models import Point, Procedure


@pytest.fixture
def material_date_query_params() -> dict[str, str]:
    return {"date_from": "2000-01-01", "date_to": "2002-01-01"}


@pytest.fixture
@freeze_time("2000-01-01 10:23:40")
def point_with_consumable_materials(factory: FixtureFactory, procedure: Procedure) -> Point:
    now = timezone.now()
    point = procedure.department.point
    stock_materials = []
    for date in [now + timedelta(days=200 * i) for i in range(1, 3)]:
        stock_material = factory.stock_material(
            stock=factory.stock(point=point, date=date.date()),
        )
        stock_materials.append(stock_material)
        for created_date in [date.date(), date.date() + timedelta(days=50)]:
            stock_materials.append(
                factory.stock_material(
                    stock=factory.stock(point=point, date=created_date),
                    material=stock_material.material,
                )
            )
    iter_date = [now] + [now + timedelta(days=i) for i in range(5)]
    for created_date in iter_date:
        for stock_material in stock_materials:
            used_material = factory.used_material(
                procedure=factory.purchase_procedure(procedure=procedure),
                material=stock_material,
            )
            used_material.created = created_date
            used_material.save()
    return point
