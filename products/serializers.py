from rest_framework import serializers
from products.models import Product, ParameterValue, ProductOnSale, Category, Parameter
from users.models import Company

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterValue
        fields = ['value']


class ProductSerializer(serializers.ModelSerializer):
    parameters = serializers.SlugRelatedField(many=True,
                                              slug_field='name',
                                              read_only=True
                                              )
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['name', 'parameters', 'category']

    def is_valid(self, raise_exception=False):
        print(self.initial_data)
        self.parameters = self.initial_data.get('parameters', [])
        self.category = self.initial_data.get('category')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(validated_data)

        product = super().create(validated_data)
        category, _ = Category.objects.get_or_create(name=self.category)
        product.category = category

        for position in self.parameters:
            parameter, _ = Parameter.objects.get_or_create(name=position['parameter'])
            ParameterValue.objects.create(parameter=parameter,
                                        value=position['value'],
                                        product_id=product.id)

        return product


# class ProductOnSaleSerializer(serializers.ModelSerializer):
#
#     shop = serializers.SlugRelatedField(
#         required=True,
#         queryset=Company.objects.all(),
#         slug_field='ITN'
#     )
#     product = ProductSerializer(required=True)
#
#     class Meta:
#         model = ProductOnSale
#         fields = '__all__'
#
#     def create(self, validated_data):
#         product = validated_data.pop('product')
#         good = super().create(validated_data)
#         good.save()
#         Product.objects.create(user=user, **contact_data)
#         return good