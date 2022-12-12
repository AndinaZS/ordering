import pytest
from rest_framework.authtoken.models import Token

from products.models import ProductItem
from users.models import User

#тест загрузки прайса
@pytest.mark.django_db
def test_products_upload(client, token, company):
    user = User.objects.get(pk=Token.objects.get(key=token).user_id)
    user.type = 'seller'
    user.company = company
    user.save()
    print(user.type, user.company.ready_to_order)
    data = {'url': 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'}
    response = client.post('/api/v1/products/loadprice/',
                           data,
                           content_type='application/json',
                           HTTP_AUTHORIZATION='Token ' + token
                           )
    assert response.status_code == 201
    assert ProductItem.objects.count() == 4
