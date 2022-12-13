from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers
from users.models import Contact, User, Company


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            value={
                'postcode': 202020,
                'city': 'Cherepovets',
                'street': 'Mira',
                'building': '55',
                'phone': '+128594789'}
        )
    ]
)
class ContactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Contact
        fields = '__all__'

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example',
            value={
                'title': 'MyCompany',
                'ITN': 1234564,
                'ready_to_order': True,
                'website': 'http://mysite.com',
                }
        )
    ]
)
class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Company
        fields = ['id', 'title', 'ITN', 'website', 'ready_to_order']

    def is_valid(self, *, raise_exception=False):
        self.user = self.initial_data.get('user')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        new_company = Company.objects.create(**validated_data)
        self.user.company = new_company
        self.user.save()
        return new_company


@extend_schema_serializer(
    exclude_fields=('id', 'company', 'contacts'),
    examples=[
        OpenApiExample(
            'Valid example',
            value={
                'username': 'testuser',
                'password': 'password1',
                'password_confirmed': 'password1',
                'email': 'example@example.com',
                'first_name': 'First',
                'last_name': 'Last'}
        )
    ]
)
class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'type']

    def is_valid(self, *, raise_exception=False):
        self.password = self.initial_data.get('password')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(self.password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        required=False,
        read_only=True,
        slug_field='ITN'
    )

    contacts = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        required=False,
        slug_field='id')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'type', 'company', 'contacts']