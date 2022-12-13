from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderPositions
from orders.permissions import IsVerified
from orders.service import send_order_message, false_positions
from orders.serializers import BasketSerializer
from users.models import Contact


class BasketView(ListCreateAPIView, DestroyAPIView):
    # класс для работы с корзиной
    serializer_class = BasketSerializer
    queryset = Order.objects.all()
    permission_classes = (IsAuthenticated, IsVerified,)

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user, state='basket')

    @extend_schema(
        responses=BasketSerializer,
        description="Return an authenticated user's basket",
        summary='Get basket'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        examples=[OpenApiExample(
            name='Valid example',
            value={"positions": [
                {"quantity": 7,
                 "good": 3},
                {"quantity": 10,
                 "good": 2}
            ]},
            request_only=True)],
        responses=BasketSerializer,
        description="Create an authenticated user's basket or updates if the basket exists",
        summary='Create basket'
    )
    def post(self, request, *args, **kwargs):
        user = self.request.user
        request.data['state'] = 'basket'
        request.data['customer'] = user.id
        return self.create(request, *args, **kwargs)

    @extend_schema(
        examples=[OpenApiExample(
            name='Valid example',
            value={"positions": [
                {"quantity": 5,
                 "good": 1},
            ]},
            request_only=True)],
        responses=BasketSerializer,
        description="Update an authenticated user's basket",
        summary='Update basket'
    )
    def put(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    @extend_schema(
        description='''Delete goods from basket. 
        Request must specify a list of goods id to delete. 
        Example {"goods": [1, 2]}. Can't be tested here''',
        summary='Delete goods'
    )
    def delete(self, request, *args, **kwargs):
        goods = request.data['goods']
        user = self.request.user
        basket = Order.objects.filter(customer=user, state='basket').first()
        for good in goods:
            item = basket.positions.filter(good=good).first()
            if item:
                item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    post=extend_schema(
        request='',
        examples=[OpenApiExample(
            name='Valid example',
            value={"contact": 1},
            request_only=True)],
        responses=BasketSerializer,
        description="Create an order from basket",
        summary='Create order'),
    get=extend_schema(
        responses=BasketSerializer,
        description="Return all user's orders (including those where he is a seller ). Authorised is required",
        summary='Get orders'
    ))
class OrderView(APIView):
    # класс для работы с заказом. доступны только создание заказа и просмотр.
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        positions = list(Order.objects.get(customer=self.request.user, state='basket').positions.all())
        res = false_positions(positions)
        if res:
            return Response({'message': f'There are not enough goods id {res} in stock'},
                            status=status.HTTP_409_CONFLICT)
        request.data['positions'] = positions
        item = Order.objects.get(customer=self.request.user, state='basket')
        item.contact = Contact.objects.get(pk=request.data['contact'])
        item.state = 'new'
        item.save()
        serializer = BasketSerializer(item)
        send_order_message(self.request.user.email, item.id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        # отдаеет заказы в которых user является покупателем или продавцом(в этом случае фильтр по позициям)
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
            print(orders)

        serializer = BasketSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
