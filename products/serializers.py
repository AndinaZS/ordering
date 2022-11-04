from rest_framework import serializers

from products.models import Product, Cathegory, PropertyValue, ProductOnSale
from users.serializers import CompanySerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Cathegory
        fields = '__all__'

class PropertyValueSerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyValue
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Cathegory.objects.all(),
        slug_field='name'
    )

    property = PropertyValueSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = '__all__'

class ProductOnSaleSerializer(serializers.ModelSerializer):

    company = CompanySerializer(required=True, read_only=True)
    product = ProductSerializer(required=True, read_only=True)

    class Meta:
        model = ProductOnSale
        fields = '__all__'