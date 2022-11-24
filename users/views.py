from authemail.models import SignupCode, send_multi_format_email
from django.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from users.models import Contact, Company
from users.permissions import CompanyOwnerPermission, IsOwnerOrReadOnly
from users.serializers import UserSerializer, ContactSerializer, CompanySerializer


class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        if request.data['password'] != request.data.get('password_confirmed'):
            return Response({'message': 'The entered passwords are different'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        user = serializer_obj.save()

        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)

        if not must_validate_email:
            user.is_verified = True
            # send_multi_format_email('welcome_email',
            #                         {'email': user.email, },
            #                         target_email=user.email)
            user.save()

        if must_validate_email:
            ipaddr = self.request.META.get('REMOTE_ADDR', '0.0.0.0')
            signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
            signup_code.send_signup_email()

        content = {'content': f'User {user.username} has been created.'}
        return Response(content, status=status.HTTP_201_CREATED)


class UserDetailChangeAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = UserSerializer
    http_method_names = ['get', 'put', 'delete']
    def get_object(self):
        obj = self.request.user
        return obj

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()
        token = Token.objects.get(user=user)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        description='Get contacts list',
        summary='Contacts list'),
    create=extend_schema(
        description='Create new contact object',
        summary='Create contact'),
    destroy=extend_schema(
        description='Delete contact',
        summary='Delete contact'),
    update=extend_schema(
            description='Update contact instance',
            summary='Update contact'),
    retrieve=extend_schema(
            description='Get contact detail',
            summary='Contact detail'),
)
class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    http_method_names = ['get', 'put', 'delete', 'post']

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = self.request.user
        request.data['user'] = user.id
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        description='Retrieve companies list',
        summary='Companies list'),
    create=extend_schema(
        description='Create new company',
        summary='Create company'),
    destroy=extend_schema(
        description='Delete company',
        summary='Delete company'),
    update=extend_schema(
            description='Update company instance',
            summary='Update company'),
    retrieve=extend_schema(
            description='Get company object detail',
            summary='Company detail'),
)
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CompanyOwnerPermission]
    queryset = Company.objects.all()
    http_method_names = ['get', 'put', 'delete', 'post']

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.data['user'] = user
        return super().create(request, *args, **kwargs)

