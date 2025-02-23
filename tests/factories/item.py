import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from todo.models import Item
from todo.models import Priority


class ItemFactory(DjangoModelFactory):
    class Meta:
        model = Item

    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
    due_date = factory.Faker("future_datetime", tzinfo=timezone.get_current_timezone())
    completed = False
    priority = factory.Iterator([Priority.LOW, Priority.MEDIUM, Priority.HIGH])
    list = factory.SubFactory("tests.factories.list.ListFactory")
