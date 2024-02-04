from app.testing import register
from app.testing.factory import FixtureFactory
from companies.models import Company


@register
def company(self: FixtureFactory, **kwargs: dict) -> Company:
    return self.mixer.blend(Company, **kwargs)


@register
def company_data(self: FixtureFactory, **kwargs: dict) -> dict:
    schema = self.schema(
        schema=lambda: {"name": self.field("text.word")},
        iterations=1,
    )
    return {**schema.create()[0], **kwargs}
