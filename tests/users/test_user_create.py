import pytest
from users.models import User



@pytest.mark.django_db
def test_create_user(client):
    expected_response ={'content':'User testuser1 has been created.'}
    data =  {'email': 'example@exammple.com',
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

