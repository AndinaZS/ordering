from rest_framework import status
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.scripts import send_order_message
from orders.serializers import BasketSerializer, OrderSerializer
from users.models import Contact


class BasketView(ListCreateAPIView):
    serializer_class = BasketSerializer
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


class OrderView(APIView):
    def post(self, request, *args, **kwargs):

        request.data['position'] = list(Order.objects.get(customer=self.request.user, state='basket').position.all())
        item = Order.objects.get(customer=self.request.user, state='basket')
        item.contact = Contact.objects.get(pk=request.data['contact'])
        item.state = 'new'
        item.save()
        seriliser = BasketSerializer(item)
        send_order_message(self.request.user.email, item.id)
        return Response(seriliser.data, status=status.HTTP_201_CREATED)




