import pytest


@pytest.fixture
@pytest.mark.django_db
def token(client, django_user_model):
    username = 'test2'
    password = 'password'
    email = '1@1.ru'
    first_name = 'Firstname'
    last_name ='Lastname'

    django_user_model.objects.create_user(
        username=username,
        email=email,
        password=password,
        password_confirmed=password,
        type='seller',
        is_verified=True,
        first_name=first_name,
        last_name=last_name
    )

    response = client.post(
        '/api/v1/login/',
        {'email': email,
         'password': password},
    )

    return response.data['token']
