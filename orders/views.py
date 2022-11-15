from django.db.models import Prefetch, Count
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderPositions
from orders.service import send_order_message
from orders.serializers import BasketSerializer
from users.models import Contact


class BasketView(ListCreateAPIView):
    serializer_class = BasketSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user, state='basket')

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
        serializer = BasketSerializer(item)
        send_order_message(self.request.user.email, item.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.type == 'customer':
            orders = Order.objects.filter(customer=self.request.user).exclude(state='basket')

        else:
            orders = Order.objects.prefetch_related(
                Prefetch(
                    "position",
                    queryset=OrderPositions.objects.filter(
                        good__shop=user.company).annotate(
                        pcount=Count('good'))
            )).exclude(state='basket').filter(position__good__shop=user.company)

        serializer = BasketSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






