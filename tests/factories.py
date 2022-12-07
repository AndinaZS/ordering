import factory.django

from users.models import User, Contact


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = 'test'
    email = 'test@test.net'
    password = 'testpassword'
    password_confirmed = password,
    is_verified = True

class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    postcode = 202020
    city = 'Cherepovets'
    street = 'Mira'
    building = '55'
    phone = '+128594789'
    user = factory.SubFactory(UserFactory)


