from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import Product, ProductItem
from products.service import get_data, ProductFilter
from products.serializers import ProductListSerializer, GoodsCreateSerializer


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(name='category', description='Filter by category', required=False, type=str),
            OpenApiParameter(name='shop', description='Filter by company', required=False, type=str),
            OpenApiParameter(name='price_max', description='Filter by max price', required=False, type=str),
            OpenApiParameter(name='price_min', description='Filter by min price', required=False, type=str)],
        description='Retrieve products list',
        summary='Products list'))
class ProductListAPIView(ListAPIView):
    '''Retrieve goods list. The list can be filtered by price rate, category, shop and ordered by price and name.'''
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
    post=extend_schema(
        examples=[OpenApiExample(
            name='Valid example',
            value={'url': 'https://raw.githubusercontent.com/netology-code/pd-diplom/master/data/shop1.yaml'},
            request_only=True)],
        responses={201: OpenApiResponse(description='created <b>num</b> positions')},
        description="""Upload products list.
        Only for authorised users with type=seller and have company ''ready_to_order""",
        summary='Upload products list'))
class ProductCreateAPIView(APIView):
    '''Allowed to upload a price. The user is required to be authorized, have type=seller
    and their company is ready_to_order. Request data has to contain link to the price list.'''
    serializer_class = GoodsCreateSerializer

    def post(self, request):
        if not self.request.user.company or self.request.user.type != 'seller':
            return Response({'message': 'Company and type "seller" are required to upload the price list'},
                            status=status.HTTP_403_FORBIDDEN)

        num = get_data(self.request, self.serializer_class)
        return Response(f'created {num} positions', status=status.HTTP_201_CREATED)
