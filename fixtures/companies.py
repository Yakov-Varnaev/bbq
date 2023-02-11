import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def auth_setup(db):

    first_user_data = {
        'username': 'first_user',
        'email': 'first_user_email@test.com',
        'password': 'Fir$t_User_password!'
    }

    second_user_data = {
        'username': 'second_user',
        'email': 'second_user_email@test.com',
        'password': '$econd_User_password!'
    }

    first_client = APIClient()
    second_client = APIClient()

    first_response = first_client.post(reverse('user-list'), data=first_user_data)
    second_response = second_client.post(reverse('user-list'), data=second_user_data)

    first_user = User.objects.get(id=first_response.data['id'])
    second_user = User.objects.get(id=second_response.data['id'])

    first_token = RefreshToken.for_user(first_user).access_token
    second_token = RefreshToken.for_user(second_user).access_token

    first_client.credentials(HTTP_AUTHORIZATION=f'Bearer {first_token}')
    second_client.credentials(HTTP_AUTHORIZATION=f'Bearer {second_token}')

    return first_client, second_client
