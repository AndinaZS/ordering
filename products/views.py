from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, ProductItem
from products.service import get_data, ProductFilter
from products.serializers import ProductListSerializer, GoodsCreateSerializer


class ProductListAPIView(ListAPIView):
    #только get, добавление товаров через загрузку прайса
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
        Prefetch("goods",
            queryset=ProductItem.objects.prefetch_related(
                'shop').filter(
                shop__ready_to_order=True))).filter(companies__ready_to_order=True)
        return queryset

class ProductCreateAPIView(APIView):
    #обрабатывает загруженный прайс
    serializer_class = GoodsCreateSerializer

    def post(self, request):
        if not self.request.user.company or self.request.user.type != 'seller':
            return Response({'message': 'Company and type "seller" are required to upload the price list'},
                            status=status.HTTP_403_FORBIDDEN)

        num = get_data(self.request, self.serializer_class)
        return Response(f'created {num} positions', status=status.HTTP_201_CREATED)