from rest_framework import serializers
from orders.models import OrderPositions, Order
from products.models import ProductItem


class ProductItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductItem
        fields = '__all__'


class OrderPositionsSerializer(serializers.ModelSerializer):
    # класс для сериализации товара в заказе + расчитываемое поле - общая стоимость товара
    total = serializers.SerializerMethodField()
    good = serializers.PrimaryKeyRelatedField(queryset=ProductItem.objects.all())

    class Meta:
        model = OrderPositions
        fields = ['good', 'quantity', 'total']

    def get_total(self, obj) -> float:
        return obj.quantity * obj.good.price


class BasketSerializer(serializers.ModelSerializer):
    # модель сериализатора для корзины и заказа
    positions = OrderPositionsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'positions', 'state']

    def create(self, validated_data):
        # создаем заказ (Order) и и связь заказа с товаром (OrderPositions)

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


