from rest_framework import serializers
from orders.models import OrderPositions, Order
from users.models import Contact


class OrderPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPositions
        fields = ['good', 'quantity']

class BasketSerializer(serializers.ModelSerializer):

    position = OrderPositionsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'position']

    def create(self, validated_data):

        print(validated_data)

        positions = validated_data.pop('position')

        order, _ = Order.objects.get_or_create(customer=validated_data['customer'], state='basket')

        for good_object in positions:
            product = order.position.filter(good=good_object['good'].id).first()

            if product:
                if good_object['quantity'] == 0:
                    product.delete()
                else:
                    product.quantity = good_object['quantity']
                    product.save()
            else:
                OrderPositions.objects.create(good=good_object['good'],
                                              quantity=good_object['quantity'],
                                              order=order)
        return order



class OrderSerializer(serializers.ModelSerializer):
    position = OrderPositionsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'state', 'position', 'contact']

    def update(self, instanse, validated_data):

        order, _ = Order.objects.get(customer=validated_data['customer'], state='basket')
        order.cintact =  validated_data['contact']
        order.state = 'new'

        return order


