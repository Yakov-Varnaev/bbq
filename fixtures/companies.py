import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from companies.models import Company

User = get_user_model()


@pytest.fixture
def company(user):
    return mixer.blend(Company, owner=user)


@pytest.fixture
def companies(user):
    return mixer.cycle(5).blend(Company, owner=user)
