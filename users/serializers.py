from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response

from users.models import Contact, User, Company

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Contact
        exclude = ('user',)

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
    contacts = ContactSerializer(many=True, required=False)
    class Meta:
        model = User
        fields = '__all__'
    def create(self, validated_data):
        contacts_data = validated_data.get('contacts', [])
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        for contact_data in contacts_data:
            Contact.objects.create(user=user, **contact_data)
        return user


