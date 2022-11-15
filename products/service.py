# from django_filters.rest_framework import FilterSet
from django_filters import FilterSet, RangeFilter, BaseInFilter, CharFilter
from requests import get
from yaml import load, Loader

from products.models import Product


class ProductFilter(FilterSet):
    category = CharFilter(field_name='category__name', lookup_expr='icontains')
    price = RangeFilter(field_name='goods__price')

    class Meta:
        model = Product
        fields = ['category', 'goods']


def get_data(request, serializer_class):
    shop = request.user.company
    url = request.data.get('url')
    price = get(url).content
    data = load(price, Loader=Loader)
    categories = {c['id']: c['name'] for c in data['categories']}
    goods = data['goods']
    for good in goods:
        parameters = [{'name': c[0], 'value': c[1]} for c in good['parameters'].items()]
        serialized_data = {
            'shop': shop.id,
            'product': {
                'category': categories[good['category']],
                'name': good['name'],
                'parameters': parameters
            },
            'price': good['price'],
            'instock': good['quantity'],
            'model': good['model'],
            'price_rrc': good['price_rrc'],
            'ext_id': good['price_rrc']
        }
        serialiser_obj = serializer_class(data=serialized_data)
        serialiser_obj.is_valid(raise_exception=True)
        serialiser_obj.save()
    return len(goods)
