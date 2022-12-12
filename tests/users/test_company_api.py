import pytest
from rest_framework.authtoken.models import Token

from tests.factories import CompanyFactory, UserFactory
from users.models import Company, User
from users.serializers import CompanySerializer


@pytest.mark.django_db
def test_create_company(client, token):

    expected_response = {
        'id': 1,
        'title': 'mycompany',
        'ITN': 98765423,
        'website': None,
        'ready_to_order': False,
    }
    data = {
        'title': 'mycompany',
        'ITN': 98765423,
    }

    response = client.post(
        '/api/v1/company/',
        data,
        HTTP_AUTHORIZATION='Token ' + token,
    )
    user = User.objects.get(pk=Token.objects.get(key=token).user_id)
    assert response.status_code == 201
    assert response.data == expected_response
    assert Company.objects.count() == 1
    assert user.company_id == 1


@pytest.mark.django_db
def test_get_company(client):
    companies = CompanyFactory.create_batch(5)
    expected_response = CompanySerializer(companies, many=True).data
    response = client.get('/api/v1/company/')

    assert Company.objects.count() == 5
    assert response.status_code == 200
    assert response.data['results'] == expected_response


@pytest.mark.django_db
def test_update_company(client, token, company):
    user = User.objects.get(pk=Token.objects.get(key=token).user_id)
    user.company = company
    user.save()
    data = {
        'title': 'NewTitle',
        'website': 'https://company.site'
    }

    response = client.patch(f'/api/v1/company/{company.id}/',
                            data,
                            content_type='application/json',
                            HTTP_AUTHORIZATION='Token ' + token
                            )
    result_obj = Company.objects.get(pk=company.id)
    assert response.status_code == 200
    assert result_obj.title == 'NewTitle'
    assert result_obj.website == 'https://company.site'


