from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSerializer

class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        user_serialiser_obj = self.serializer_class(data=request.data)
        user_serialiser_obj.is_valid(raise_exception=True)
        validated_data = user_serialiser_obj.validated_data
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

        if not must_validate_email:
            user.is_verified = True
            # send_multi_format_email('welcome_email',
            #                         {'email': user.email, },
            #                         target_email=user.email)
        user.save()

        # if must_validate_email:
        # ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
        # signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
        # signup_code.send_signup_email()

        content = {'email': user.email}
        return Response(content, status=status.HTTP_201_CREATED)


