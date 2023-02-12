import pytest
import json
from rest_framework import status
from django.urls import reverse
from companies.models import Company
from companies.serializers import CompanySerializer


@pytest.mark.django_db
class TestCRUD:

    def test_retrieve(self, company, auth_client):

        company.save()

        response = auth_client.get(reverse('companies-detail', args=[company.id]))

        assert response.status_code == status.HTTP_200_OK

        db_data = CompanySerializer(company).data
        response_data = json.loads(response.content)

        assert db_data == response_data

    def test_get_list(self, multiple_companies, auth_client):

        for company in multiple_companies:
            company.save()

        response = auth_client.get(reverse('companies-list'))

        assert response.status_code == status.HTTP_200_OK

        db_data = CompanySerializer(Company.objects.all(), many=True).data
        response_data = json.loads(response.content)

        assert db_data == response_data

    def test_post(self, auth_client):
        post_data = {'name': 'TestCompany'}
        response = auth_client.post(reverse('companies-list'), data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

    def test_put(self, company, auth_client, auth_unauthorized_client):
        put_data = {'name': 'TestCompany2'}
        company_uri = reverse('companies-detail', args=[company.id])

        assert auth_client.put(company_uri, data=put_data).status_code == status.HTTP_200_OK
        assert auth_unauthorized_client.put(company_uri, data=put_data).status_code != status.HTTP_200_OK

    def test_delete(self, company, auth_client, auth_unauthorized_client):
        company_uri = reverse('companies-detail', args=[company.id])

        assert auth_unauthorized_client.delete(company_uri).status_code != status.HTTP_204_NO_CONTENT
        assert auth_client.delete(company_uri).status_code == status.HTTP_204_NO_CONTENT
