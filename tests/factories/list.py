import factory
from factory.django import DjangoModelFactory

from todo.models import List


class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    owner = factory.SubFactory("tests.factories.user.UserFactory")
