import pytest


@pytest.mark.django_db
def test_create_contact(client, token):
    expected_response = {
        "postcode": 202020,
        "city": "Cherepovets",
        "street": "Mira",
        "building": "55",
        "phone": "+128594789"
    }
    data = {
        "postcode": 202020,
        "city": "Cherepovets",
        "street": "Mira",
        "building": "55",
        "phone": "+128594789"
    }

    response = client.post(
        '/api/v1/users/me/contact/',
        data,
        HTTP_AUTHORIZATION='Token ' + token,
        content_type='application/json')
    assert response.status_code == 201