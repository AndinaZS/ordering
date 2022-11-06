from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from products.models import ProductOnSale, ParameterValue, Product
from products.serializers import ProductSerializer, ProductSerializer


# class ProductListCreateApiView(ListCreateAPIView):
#     serializer_class = ProductOnSaleSerializer
#     queryset = ProductOnSale.objects.all()
#     permission_classes = [IsAuthenticatedOrReadOnly,]

class ProductCreateAPIView(ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()