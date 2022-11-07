from requests import get
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from yaml import load, Loader

from products.models import ProductOnSale, Product
from products.serializers import ProductListSerializer, GoodsCreateSerializer


class ProductListAPIView(ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()


class ProductCreateAPIView(APIView):
    serializer_class = GoodsCreateSerializer
    def post(self, request, *args, **kwargs):
        shop = self.request.user.company
        url = request.data.get('url')
        price = get(url).content
        data = load(price, Loader=Loader)
        categories = {c['id']: c['name'] for c in data['categories']}
        goods = data['goods']
        for good in goods:
            parameters = [{"name":c[0], "value":c[1]} for c in good['parameters'].items()]
            serialized_data = {
                "shop":shop.id,
                "product":{
                    "category":categories[good['category']],
                    "name":good['name'],
                    "parameters":parameters
                },
                "price":good['price'],
                'quantity':good['quantity']
            }
            serialiser_obj = self.serializer_class(data=serialized_data)
            serialiser_obj.is_valid(raise_exception=True)
            good = serialiser_obj.save()
        return Response(f'created {len(goods)} positions', status=status.HTTP_201_CREATED)


