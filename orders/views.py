from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import OrderPositions, Order
from orders.serializers import OrderSerializer
from products.models import Product
from users.models import Company


class CreateOrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    # def get_queryset(self):
    #     user = self.request.user
    #     return Order.objects.filter(customer=user).filter(state='basket')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if Order.objects.filter(customer=user).filter(state='basket'):
            return Response({'message':'Can not create one more basket for this user. Use PATCH for update'},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        request.data['state'] = 'basket'
        request.data['customer'] = user.id
        return self.create(request, *args, **kwargs)


class UpdateOrderView(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def update(self, request, *args, **kwargs):
        request.data['customer'] = self.request.user.id
        return super(UpdateOrderView, self).update(request, *args, **kwargs)
    #
    # def get_object(self):
    #     user = self.request.user
    #     instance = Order.objects.filter(customer=user).filter(state='basket').first()
    #     return instance





