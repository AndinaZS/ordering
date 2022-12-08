import pytest


@pytest.fixture
@pytest.mark.django_db
def token(client, user):

    response = client.post(
        '/api/v1/login/',
        {'email': user.email,
         'password': 'testpassword'},
    )

    return response.data['token']
