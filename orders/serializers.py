from rest_framework import serializers
from orders.models import OrderPositions, Order

class OrderPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPositions
        fields = ['good', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    position = OrderPositionsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'state', 'contact', 'position']

    def create(self, validated_data):

        positions = validated_data.pop('position')

        order = super().create(validated_data)

        for position in positions:
            OrderPositions.objects.create(good=position['good'],
                                        quantity=position['quantity'],
                                        order=order)

        return order

    def update(self, instance, validated_data):

        positions = validated_data.pop('position')

        order = super().update(instance, validated_data)

        for object in positions:
            product = order.position.filter(good=object['good'].id).first()

            if product:
                if object['quantity'] == 0:
                    product.delete()
                else:
                    product.quantity = object['quantity']
                    product.save()
            else:
                OrderPositions.objects.create(good=object['good'],
                                            quantity=object['quantity'],
                                            order=order)
            order.save()
        return order

