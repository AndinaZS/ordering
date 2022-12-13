from rest_framework import serializers
from orders.models import OrderPositions, Order
from products.models import ProductItem


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'


class OrderPositionsSerializer(serializers.ModelSerializer):
    """ the class for serializing products in the order.
    'total' is additional calculated field as total cost of the product
    """
    total = serializers.SerializerMethodField()
    good = serializers.PrimaryKeyRelatedField(queryset=ProductItem.objects.all())

    class Meta:
        model = OrderPositions
        fields = ['good', 'quantity', 'total']

    def get_total(self, obj) -> float:
        return obj.quantity * obj.good.price


class BasketSerializer(serializers.ModelSerializer):
    """This Serializer is used for Basket and Order"""
    positions = OrderPositionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'positions', 'state']

    def create(self, validated_data):
        """function response to create Orders connect them with OrderPositions"""

        positions = validated_data.pop('positions')
        order, _ = Order.objects.get_or_create(customer=validated_data['customer'], state='basket')

        for position in positions:
            product = order.positions.filter(good=position['good']).first()
            if product:
                if position['quantity'] == 0:
                    product.delete()
                else:
                    product.quantity = position['quantity']
                    product.save()
            else:
                OrderPositions.objects.create(good=position['good'],
                                              quantity=position['quantity'],
                                              order=order)
        return order


