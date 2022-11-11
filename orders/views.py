from rest_framework.generics import ListCreateAPIView


from orders.models import Order
from orders.serializers import OrderSerializer

class BasketView(ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user).filter(state='basket')

    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['state'] = 'basket'
        request.data['customer'] = user.id
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)






