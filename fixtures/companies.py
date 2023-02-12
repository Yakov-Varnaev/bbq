import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from companies.models import CompanyModel

User = get_user_model()


@pytest.fixture
def company(user):
    return mixer.blend(CompanyModel, owner=user)

