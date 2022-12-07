import pytest
from rest_framework.authtoken.models import Token

from users.models import Contact
from users.serializers import ContactSerializer


@pytest.mark.django_db
def test_create_contact(client, token):
    expected_response = {
        'id': 1,
        'postcode': 202020,
        'city': 'Cherepovets',
        'street': 'Mira',
        'building': '55',
        'phone': '+128594789',
        'apartment': '',
        'additional_info': None,
        'region': '',
        'user': Token.objects.get(key=token).user_id
    }
    data = {
        'postcode': 202020,
        'city': 'Cherepovets',
        'street': "Mira",
        'building': '55',
        'phone': '+128594789'
    }

    response = client.post(
        '/api/v1/users/me/contact/',
        data,
        HTTP_AUTHORIZATION='Token ' + token,
    )
    assert response.status_code == 201
    assert response.data == expected_response
    assert Contact.objects.count() == 1


@pytest.mark.django_db
def test_get_contact(client, token, contact):
    response = client.get('/api/v1/users/me/contact/',
                          HTTP_AUTHORIZATION='Token ' + token
                          )
    expected_response = [
            {'id': contact.id,
             'postcode': 202020,
             'region': '',
             'city': 'Cherepovets',
             'street': 'Mira',
             'building': '55',
             'apartment': '',
             'additional_info': None,
             'phone': '+128594789',
             'user': contact.user_id}]

    assert Contact.objects.count() == 1
    assert response.status_code == 200
    assert response.data['results'] == expected_response

@pytest.mark.django_db
def test_update_contact(client, token, contact):

    data = {
        'city': 'Vologda',
        'additional_info': 'I moved!!!'
    }

    response = client.patch(f'/api/v1/users/me/contact/{contact.id}/',
                          data,
                          content_type='application/json',
                          HTTP_AUTHORIZATION='Token ' + token
                          )
    result_obj = Contact.objects.get(pk=contact.id)
    assert response.status_code == 200
    assert result_obj.city == 'Vologda'
    assert result_obj.additional_info == 'I moved!!!'

@pytest.mark.django_db
def test_delete_contact(client, token, contact):
    response = client.delete(f'/api/v1/users/me/contact/{contact.id}/',
                            content_type='application/json',
                            HTTP_AUTHORIZATION='Token ' + token
                            )
    assert response.status_code == 204
    assert not Contact.objects.filter(pk=contact.id)


