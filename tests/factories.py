import factory.django
from django.conf import settings
from django.contrib.auth.hashers import make_password

from users.models import User, Contact


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = 'test'
    email = 'test@test.net'
    password = make_password('123')
    is_verified = True
    first_name = 'test'
    last_name = 'test'


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    postcode = 202020
    city = 'Cherepovets'
    street = 'Mira'
    building = '55'
    phone = '+128594789'
    user = factory.SubFactory(UserFactory)
