import pytest
import json
from rest_framework import status
from django.urls import reverse
from companies.models import Company
from companies.serializers import CompanySerializer


@pytest.mark.django_db
class TestCRUD:

    def test_retrieve(self, company, auth_client):

        response = auth_client.get(reverse('companies-detail', args=[company.id]))

        assert response.status_code == status.HTTP_200_OK

        db_data = CompanySerializer(company).data
        response_data = json.loads(response.content)

        assert db_data == response_data

    def test_get_list(self, multiple_companies, auth_client):

        response = auth_client.get(reverse('companies-list'))

        assert response.status_code == status.HTTP_200_OK

        db_data = CompanySerializer(Company.objects.all(), many=True).data
        response_data = json.loads(response.content)

        assert db_data == response_data

    def test_post(self, auth_client):

        post_data = {'name': 'TestCompany'}
        response = auth_client.post(reverse('companies-list'), data=post_data)

        assert response.status_code == status.HTTP_201_CREATED

        response_data = json.loads(response.content)
        company_id = response_data['id']

        db_data = CompanySerializer(Company.objects.get(id=company_id)).data

        assert db_data == response_data

    def test_put(self, company, auth_client, auth_unauthorized_client):

        put_data = {'name': 'TestCompany'}
        company_uri = reverse('companies-detail', args=[company.id])

        response = auth_client.put(company_uri, data=put_data)

        assert response.status_code == status.HTTP_200_OK
        assert auth_unauthorized_client.put(company_uri, data=put_data).status_code != status.HTTP_200_OK

        response_data = json.loads(response.content)
        company_id = response_data['id']

        db_data = CompanySerializer(Company.objects.get(id=company_id)).data

        assert db_data == response_data

    def test_delete(self, company, auth_client, auth_unauthorized_client):

        company_uri = reverse('companies-detail', args=[company.id])
        assert auth_unauthorized_client.delete(company_uri).status_code != status.HTTP_204_NO_CONTENT

        response = auth_client.delete(company_uri)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b''

        with pytest.raises(Company.DoesNotExist):
            CompanySerializer(Company.objects.get(id=company.id))
