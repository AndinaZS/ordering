from rest_framework.generics import CreateAPIView, UpdateAPIView, ListCreateAPIView

from orders.models import OrderPositions, Order
from orders.serializers import OrderSerializer


class CreateOrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    # queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)

    def post(self, request, *args, **kwargs):
        request.data['state'] = 'basket'
        request.data['customer'] = self.request.user.id
        return self.create(request, *args, **kwargs)


class UpdateOrderView(UpdateAPIView):
    serializer_class = OrderSerializer
    queryset = OrderPositions.objects.all()


