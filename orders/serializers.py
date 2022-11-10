from rest_framework import serializers

from orders.models import OrderPositions, Order
from products.models import ProductOnSale


# # class ProductOnSaleSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = ProductOnSale
# #         fields = ['product', 'price']
#
# class OrderPositionsSerializer(serializers.ModelSerializer):
#
#     # good = serializers.PrimaryKeyRelatedField(read_only=True)
#     class Meta:
#         model = OrderPositions
#         fields = '__all__'
#
# class OrderSerializer(serializers.ModelSerializer):
#
#     positions = OrderPositionsSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ['id', 'state', 'positions']

# def create(self, validated_data):
#     positions = validated_data.pop('positions')
#
#     order = super().create(validated_data)
#
#     for position in positions:
#         OrderPositions.objects.create(product=position['product'],
#                                     quantity=position['quantity'],
#                                     order=order)
#
#     return order
#
# def update(self, instance, validated_data):
#
#     # def is_valid(self, raise_exception=False):
#     #     self.positions = self.initial_data.get('positions', [])
#     #     return super().is_valid(raise_exception=raise_exception)
#     positions = validated_data.pop('positions')
#
#     order = super().update(instance, validated_data)
#
#     for position in positions:
#         product = order.positions.filter(id=position['product'].id)[0]
#         print(product)
#
#         if product:
#             if position['quantity'] == 0:
#                 product.delete()
#             else:
#                 product.__class__.objects.update(quantity=position['quantity'])
#         else:
#             OrderPositions.objects.create(product=position['product'],
#                                         quantity=position['quantity'],
#                                         order=order)
#         order.save()
#     return order

# def partial_update(self, instance, validated_data):
#     pass

class OrderPositionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPositions
        fields = '__all__'

class GoodSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    position = OrderPositionsSerializer(many=True)

    class Meta:
        model = ProductOnSale
        fields = ['id', 'product', 'price', 'position']
        # fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    positions = GoodSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'positions']
