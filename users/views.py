from django.conf import settings
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from users.models import Contact
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer, ContactSerializer


class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        serialiser_obj = self.serializer_class(data=request.data)
        serialiser_obj.is_valid(raise_exception=True)
        user = serialiser_obj.save()

        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

        if not must_validate_email:
            user.is_verified = True
        #     # send_multi_format_email('welcome_email',
        #     #                         {'email': user.email, },
        #     #                         target_email=user.email)
            user.save()
        #
        # # if must_validate_email:
        # # ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
        # # signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
        # # signup_code.send_signup_email()
        #
        content = {'content': f'User {user.username} creaated.'}
        return Response(content, status=status.HTTP_201_CREATED)

class ContactListCreateApiView(ListCreateAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated,]
    queryset = Contact.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactDetailUpdateDelApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Contact.objects.all()
