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

    def is_valid(self, *, raise_exception=False):
        self.user = self.initial_data.get('user')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_company = Company.objects.create(**validated_data)
        self.user.company = new_company
        self.user.save()
        return new_company


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
        contacts_data = validated_data.pop('contacts') if validated_data.get('contacts') else []
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        for contact_data in contacts_data:
            Contact.objects.create(user=user, **contact_data)
        return user
