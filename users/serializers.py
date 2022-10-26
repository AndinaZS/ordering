import json

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        self.send_token(user)
        return user
    def send_token(self, user):
        # current_site = get_current_site(request)
        message = json.dumps({
            'user': user.username,
            #'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        mail_subject = 'Activate your blog account.'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()
        return None