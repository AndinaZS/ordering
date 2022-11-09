from rest_framework import serializers

from orders.models import OrderPositions, Order
from products.serializers import GoodsCreateSerializer


class OrderPositionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPositions
        exclude = ['order']

class OrderSerializer(serializers.ModelSerializer):

    positions = OrderPositionsSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        positions = validated_data.pop('positions')

        order = super().create(validated_data)

        for position in positions:
            OrderPositions.objects.create(product=position['product'],
                                        quantity=position['quantity'],
                                        order=order)

        return order

