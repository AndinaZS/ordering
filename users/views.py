import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer

class RegisterApiView(APIView):
    serializer_class = UserSerializer
    model = User

    def post(self, request):
        user_serialiser_obj = self.serializer_class(data=request.data)
        user_serialiser_obj.is_valid(raise_exception=True)
        validated_data = user_serialiser_obj.validated_data
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        # user.save()
        # self.send_verification(user, request)
        return redirect('/confirm_email/')

    def send_verification(self, user, request):
        current_site = get_current_site(request)
        message = json.dumps({
            'user': user.username,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user)
        })
        mail_subject = 'Activate your blog account.'
        email = EmailMessage(mail_subject, message, to=[user.email])
        email.send()

    def user_login(self, request):
        user = authenticate(email=request.data['email'], password=request.data['password'])
        login(request, user)
        print(user.is_authenticated)


class VerifiedApiView(APIView):

    def get(self, request):
        return Response(data='to complete the registration, confirm your email',
                        status=status.HTTP_201_CREATED)
    def post(self, request):
        return Response(data='post test')
