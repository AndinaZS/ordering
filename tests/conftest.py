from pytest_factoryboy import register

from tests.factories import UserFactory, ContactFactory

#fixtures
pytest_plugins = 'tests.fixtures'

#factories
register(UserFactory)
register(ContactFactory)