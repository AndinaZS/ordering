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


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    company = serializers.SlugRelatedField(
        required=False,
        queryset=Company.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        self.company = self.initial_data.get('company')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        if self.company:
            company = Company.objects.get_or_create(title=self.company['title'],
                                                    ITN=self.company['ITN'],
                                                    website=self.company.get['website'],
                                                    ready_to_order=self.company.get['ready_to_order', False]
                                                    )
        user.save()
        return user