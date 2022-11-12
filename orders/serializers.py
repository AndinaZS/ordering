from rest_framework import serializers
from orders.models import OrderPositions, Order
from products.models import ProductOnSale
from users.models import Contact

class ProductOnSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOnSale
        fields = '__all__'

class TotalField(serializers.Field):
    def to_representation(self, value):
        total = value.quantity * value.good.price
        return total

class OrderPositionsSerializer(serializers.ModelSerializer):
    total = TotalField(source='*')
    good = ProductOnSaleSerializer(read_only=True)
    class Meta:
        model = OrderPositions
        fields = ['good', 'quantity', 'total']

class BasketSerializer(serializers.ModelSerializer):

    position = OrderPositionsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'position', 'state']

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


