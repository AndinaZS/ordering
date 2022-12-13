from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from social_django.models import UserSocialAuth

from ordering import settings
from users.models import Contact, Company
from users.permissions import CompanyOwnerPermission, IsOwnerOrReadOnly, UserOrReadOnly
from users.serializers import UserSerializer, ContactSerializer, CompanySerializer


@extend_schema(
    request=UserSerializer,
    responses={201: OpenApiResponse(description='User username has been created.')},
    description="Create new user. If AUTH_EMAIL_VERIFICATION=True, user.is_verified=False",
    summary='Create user'
)
class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        if request.data['password'] != request.data.get('password_confirmed'):
            return Response({'message': 'The entered passwords are different'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        serializer_obj = self.serializer_class(data=request.data)
        serializer_obj.is_valid(raise_exception=True)
        user = serializer_obj.save()
        content = {'content': f'User {user.username} has been created.'}
        return Response(content, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description='Get user detail. Authentication is required',
        summary='User detail'),
    delete=extend_schema(
        description="Delete user (set user.is_active=False, delete user's token).Authentication is required.",
        summary='Delete user'),
    patch=extend_schema(
            description='Change user data. Authentication is required',
            summary='Update user'),
)
class UserDetailChangeAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, UserOrReadOnly]
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'delete']
    def get_object(self):
        obj = self.request.user
        return obj

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.is_verified = False
        user.save()
        token = Token.objects.filter(user=user).first()
        if token:
            token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema_view(
    list=extend_schema(
        description="Return user's contacts. Authentication is required.",
        summary='Contacts list'),
    create=extend_schema(
        description='Create new contact object. Authentication is required.',
        summary='Create contact'),
    destroy=extend_schema(
        description='Delete contact. Authentication is required.',
        summary='Delete contact'),
    partial_update=extend_schema(
            description='Update contact instance. Authentication is required.',
            summary='Update contact'),
    retrieve=extend_schema(
            description='Get contact detail. Authentication is required.',
            summary='Contact detail'),
)
class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        queryset = Contact.objects.filter(user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.POST._mutable = True
        request.data['user'] = user.id
        request.POST._mutable = False
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    list=extend_schema(
        description='Retrieve companies list',
        summary='Companies list'),
    create=extend_schema(
        description='Create new company. Authentication is required.',
        summary='Create company'),
    destroy=extend_schema(
        description='Delete company. Authentication is required.',
        summary='Delete company'),
    partial_update=extend_schema(
            description='Update company instance. Authentication is required.',
            summary='Update company'),
    retrieve=extend_schema(
            description='Get company object detail',
            summary='Company detail'),
)
class CompanyViewSet(ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, CompanyOwnerPermission]
    queryset = Company.objects.all()
    http_method_names = ['get', 'patch', 'delete', 'post']

    def create(self, request, *args, **kwargs):
        user = self.request.user
        request.POST._mutable = True
        request.data['user'] = user
        request.POST._mutable = False
        return super().create(request, *args, **kwargs)
