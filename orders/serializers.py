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

    def update(self, instance, validated_data):

        # def is_valid(self, raise_exception=False):
        #     self.positions = self.initial_data.get('positions', [])
        #     return super().is_valid(raise_exception=raise_exception)
        positions = validated_data.pop('positions')

        order = super().update(instance, validated_data)

        for position in positions:
            product = order.positions.all()

            if product:
                if position['quantity'] == 0:
                    product.delete()
                else:
                    product.update(quantity=position['quantity'])
            else:
                OrderPositions.objects.create(product=position['product'],
                                            quantity=position['quantity'],
                                            order=order)
            order.save()
        return order

    # def partial_update(self, instance, validated_data):
    #     pass