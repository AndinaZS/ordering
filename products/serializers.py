from rest_framework import serializers
from products.models import Product, ParameterValue, ProductOnSale, Category, Parameter
from users.models import Company

class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterValue
        fields = ['value']


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

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['title']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']
class GoodsSerializer(serializers.ModelSerializer):
    shop = CompanySerializer()
    class Meta:
        model = ProductOnSale
        exclude = ('product', )
class ProductListSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=True)
    category = CategorySerializer()
    values = ProductPositionSerializer(many=True)
    class Meta:
        model = Product
        fields = ['name', 'category', 'values', 'goods']


# class ProductListSerializer(serializers.ModelSerializer):
#     product = ProductSerializer()
#     shop = CompanySerializer()
#     class Meta:
#         model = ProductOnSale
#         fields = '__all__'

class GoodsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOnSale
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