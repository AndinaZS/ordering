from rest_framework import serializers

from users.models import Contact, User, Company

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Contact
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Company
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    company = serializers.SlugRelatedField(
        required=False,
        queryset=Company.objects.all(),
        slug_field='ITN'
    )

    class Meta:
        model = User
        fields = '__all__'
