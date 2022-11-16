from rest_framework import serializers
from products.models import Product, ParameterValue, ProductItem, Category, Parameter


class ParameterValueSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()
    class Meta:
        model = ParameterValue
        fields = ['parameter', 'value']


class GoodsSerializer(serializers.ModelSerializer):
    shop = serializers.StringRelatedField()

    class Meta:
        model = ProductItem
        exclude = ['product','id']


class ProductCreateSerializer(serializers.ModelSerializer):
    parameters = serializers.SlugRelatedField(many=True,
                                              slug_field='name',
                                              read_only=True
                                              )
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['name', 'parameters', 'category']

    def is_valid(self, raise_exception=False):
        self.parameters = self.initial_data.get('parameters', [])
        self.category = self.initial_data.get('category')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        #создает товар и при необходимости категорию и свойство. по API не доступна
        #только через GoodsCreateSerializer при загрузки прайса
        product = super().create(validated_data)
        category, _ = Category.objects.get_or_create(name=self.category)
        product.category = category
        product.save()

        for parameter in self.parameters:
            parameter_obj, _ = Parameter.objects.get_or_create(name=parameter['name'])
            ParameterValue.objects.create(parameter=parameter_obj,
                                          value=parameter['value'],
                                          product_id=product.id)

        return product


class ProductListSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=True)
    category = serializers.StringRelatedField()
    values = ParameterValueSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'values', 'goods']



class GoodsCreateSerializer(serializers.ModelSerializer):
    #сериализация связки товар-магазин
    class Meta:
        model = ProductItem
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        if not Product.objects.filter(name=self.initial_data['product']['name']).first():
            serialiser_obj = ProductCreateSerializer(data=self.initial_data['product'])
            serialiser_obj.is_valid(raise_exception=True)
            product = serialiser_obj.save()
        else:
            product = Product.objects.filter(name=self.initial_data['product']['name']).first()
        self.initial_data['product'] = product.id
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        good = super().create(validated_data)
        return good
