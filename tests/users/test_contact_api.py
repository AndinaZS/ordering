import pytest
from rest_framework.authtoken.models import Token

from users.models import Contact


@pytest.mark.django_db
def test_create_contact(client, token):
    expected_response = {
        'id':1,
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


# @pytest.mark.django_db
# def test_get_contact(client, token):
#     response = client.get('/api/v1/users/me/contact/',
#                           HTTP_AUTHORIZATION='Token ' + token)
#     expected_response = {
#         "postcode": 202020,
#         "city": "Cherepovets",
#         "street": "Mira",
#         "building": "55",
#         "phone": "+128594789"
#     }
#     assert Contact.objects.count() == 1
#     assert response.status_code == 200
#     assert response.data == expected_response