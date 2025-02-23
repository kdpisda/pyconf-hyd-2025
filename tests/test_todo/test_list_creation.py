from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories.list import ListFactory
from tests.factories.user import UserFactory
from todo.models import List


class TestListCreation(TestCase):
    def setUp(self):
        """Setup runs before each test method"""
        super().setUp()
        self.client = APIClient()
        self.user = UserFactory()
        self.admin_user = UserFactory(
            username="admin", is_staff=True, is_superuser=True
        )
        self.base_url = reverse("list-list")

    def authenticate_user(self, user):
        """Helper method to authenticate a user"""
        self.client.force_authenticate(user=user)

    def test_create_list_authenticated(self):
        """Test creating a new list when authenticated"""
        # Arrange
        self.authenticate_user(self.user)
        payload = ListFactory.build(owner=None).__dict__
        payload.pop("id", None)  # Remove id field if present
        payload.pop("created_at", None)  # Remove created_at field

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert List.objects.count() == 1
        list_obj = List.objects.first()
        assert list_obj.title == payload["title"]
        assert list_obj.description == payload["description"]

    def test_create_list_unauthenticated(self):
        """Test creating a list fails when not authenticated"""
        # Arrange
        payload = ListFactory.build(owner=None).__dict__
        payload.pop("id", None)
        payload.pop("created_at", None)

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert List.objects.count() == 0

    def test_list_owner_is_creator(self):
        """Test that the list owner is set to the authenticated user"""
        # Arrange
        self.authenticate_user(self.user)
        payload = ListFactory.build(owner=None).__dict__
        payload.pop("id", None)
        payload.pop("created_at", None)

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        list_obj = List.objects.first()
        assert list_obj.owner == self.user

    def test_admin_can_see_all_lists(self):
        """Test that admin users can see all lists"""
        # Arrange
        user_list = ListFactory(owner=self.user)
        admin_list = ListFactory(owner=self.admin_user)

        # Authenticate as admin
        self.authenticate_user(self.admin_user)

        # Act
        response = self.client.get(self.base_url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Should see both lists
        list_titles = {item["title"] for item in response.data}
        assert user_list.title in list_titles
        assert admin_list.title in list_titles

    def test_user_can_only_see_own_lists(self):
        """Test that regular users can only see their own lists"""
        # Arrange
        user_list = ListFactory(owner=self.user)

        # Authenticate as regular user
        self.authenticate_user(self.user)

        # Act
        response = self.client.get(self.base_url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Should only see their own list
        assert response.data[0]["title"] == user_list.title
