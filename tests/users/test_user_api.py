import pytest
from rest_framework.authtoken.models import Token

from users.models import User
from users.serializers import UserSerializer


@pytest.mark.django_db
def test_create_user(client):
    expected_response = {'content': 'User testuser1 has been created.'}
    data = {'email': 'example@exammple.com',
            'username': 'testuser1',
            'password': 'userpassword1',
            'password_confirmed': 'userpassword1',
            'first_name': 'Firtname',
            'last_name': 'Lastname'}
    response = client.post('/api/v1/signup/',
                           data,
                           content_type='application/json')

    assert response.status_code == 201
    assert response.data == expected_response
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_get_user(client, token):
    user = User.objects.get(pk=Token.objects.get(key=token).user_id)
    response = client.get('/api/v1/users/me/',
                          HTTP_AUTHORIZATION='Token ' + token)

    assert response.status_code == 200
    assert response.data == UserSerializer(user).data


@pytest.mark.django_db
def test_update_user(client, token):
    data = {
        'first_name': 'NewFirstname',
        'type': 'customer'
    }
    response = client.patch('/api/v1/users/me/',
                            data,
                            content_type='application/json',
                            HTTP_AUTHORIZATION='Token ' + token)
    user = User.objects.get(pk=Token.objects.get(key=token).user_id)
    assert response.status_code == 200
    assert user.first_name == 'NewFirstname'
    assert user.type == 'customer'


@pytest.mark.django_db
def test_delete_user(client, token):
    id = Token.objects.get(key=token).user_id
    response = client.delete('/api/v1/users/me/',
                             HTTP_AUTHORIZATION='Token ' + token)

    assert response.status_code == 204
    assert not Token.objects.filter(key=token)
    assert User.objects.get(pk=id).is_active == False


@pytest.mark.django_db
def test_login_user(client, user):

    response = client.post(
        '/api/v1/login/',
        {'email': 'test@test.net',
         'password': '123'}
    )

    assert response.status_code == 200
    assert response.data['token']
