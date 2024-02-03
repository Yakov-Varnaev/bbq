import pytest

from companies.api.fields import LowercaseCharField


@pytest.fixture
def lowercase_char_field() -> LowercaseCharField:
    return LowercaseCharField()
