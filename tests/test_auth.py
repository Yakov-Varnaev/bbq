import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserAuth:

    def test_user_can_register(self, client: APIClient):
        data = {
            'username': 'epicker',
            'email': 'epicker@test.com',
            'password': 's0meHard1',
        }
        response = client.post(reverse('user-list'), data=data)

        assert response.status_code == status.HTTP_201_CREATED, response
        assert response.data == {
            'username': 'epicker',
            'email': 'epicker@test.com',
            'id': 1,
        }

    def test_get_me(self, auth_client):
        response = auth_client.get(reverse('user-me'))

        assert response.status_code == status.HTTP_200_OK, response.data

