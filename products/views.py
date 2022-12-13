from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, ProductItem
from products.service import get_data, ProductFilter
from products.serializers import ProductListSerializer, GoodsCreateSerializer


@extend_schema_view(
    list=extend_schema(
        description='Retrieve products list',
        summary='Products list'))
class ProductListAPIView(ListAPIView):
    #полученеи списка товаров
    serializer_class = ProductListSerializer
    queryset = Product.objects.prefetch_related('goods').select_related('company')
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ('goods__price', 'name')

    def get_queryset(self):
        queryset = Product.objects.prefetch_related(
        Prefetch("goods",
            queryset=ProductItem.objects.prefetch_related(
                'shop').filter(
                shop__ready_to_order=True))).filter(companies__ready_to_order=True)
        return queryset
@extend_schema_view(
    create=extend_schema(
        description='Upload products list. ',
        summary='Products list'))
class ProductCreateAPIView(APIView):
    #обрабатывает загруженный прайс
    serializer_class = GoodsCreateSerializer

    def post(self, request):
        if not self.request.user.company or self.request.user.type != 'seller':
            return Response({'message': 'Company and type "seller" are required to upload the price list'},
                            status=status.HTTP_403_FORBIDDEN)

        num = get_data(self.request, self.serializer_class)
        return Response(f'created {num} positions', status=status.HTTP_201_CREATED)