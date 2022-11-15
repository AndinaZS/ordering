from django.db.models import Prefetch
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderPositions
from orders.service import send_order_message, false_positions
from orders.serializers import BasketSerializer
from users.models import Contact


class BasketView(ListCreateAPIView):
    serializer_class = BasketSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)

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

    def delete(self, request, *args, **kwargs):
        positions = request.data['positions']
        user = self.request.user
        basket = Order.objects.filter(customer=user, state='basket').first()
        for position in positions:
            item = basket.positions.filter(good=position).first()
            if item:
                item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        positions = list(Order.objects.get(customer=self.request.user, state='basket').positions.all())
        res = false_positions(positions)
        print(res)
        if res:
            return Response({'message':f'There are not enough goods id {res} in stock'}, status=status.HTTP_409_CONFLICT)
        request.data['positions'] = positions
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
                    "positions",
                    queryset=OrderPositions.objects.prefetch_related('good').filter(
                        good__shop=user.company)
            )).exclude(state='basket').filter(positions__good__shop=user.company)

        serializer = BasketSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






