import factory.django
from django.conf import settings
from django.contrib.auth.hashers import make_password

from products.models import Category
from users.models import Contact, Company


# для приложения users

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = make_password('testpassword')
    is_verified = True
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    title = factory.Faker('company')
    ITN = factory.Faker('random_int')
    ready_to_order = True
    # users = factory.RelatedFactory(UserFactory,
    #                                factory_related_name='user')


class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    postcode = 202020
    city = 'Cherepovets'
    street = 'Mira'
    building = '55'
    phone = '+128594789'
    user = factory.SubFactory(UserFactory)


# для приложения products
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'смартфоны'
