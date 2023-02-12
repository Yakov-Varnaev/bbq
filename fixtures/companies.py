import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from companies.models import CompaniesModel

User = get_user_model()


@pytest.fixture
def company(user):
    return mixer.blend(CompaniesModel, owner=user)

