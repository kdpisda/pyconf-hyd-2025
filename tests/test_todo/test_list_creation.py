from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from todo.models import List


class TestListCreation(TestCase):
    def setUp(self):
        """Setup runs before each test method"""
        super().setUp()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        self.admin_user = User.objects.create_superuser(
            username="admin", password="admin123", email="admin@example.com"
        )
        self.base_url = reverse("list-list")  # DRF's router convention: {basename}-list

    def authenticate_user(self, user):
        """Helper method to authenticate a user"""
        self.client.force_authenticate(user=user)

    def test_create_list_authenticated(self):
        """Test creating a new list when authenticated"""
        # Arrange
        self.authenticate_user(self.user)
        payload = {"title": "My Test List", "description": "A test list description"}

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
        payload = {"title": "My Test List", "description": "A test list description"}

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert List.objects.count() == 0

    def test_list_owner_is_creator(self):
        """Test that the list owner is set to the authenticated user"""
        # Arrange
        self.authenticate_user(self.user)
        payload = {"title": "My Test List", "description": "A test list description"}

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        list_obj = List.objects.first()
        assert list_obj.owner == self.user

    def test_admin_can_see_all_lists(self):
        """Test that admin users can see all lists"""
        # Arrange
        # Create a list for regular user
        self.authenticate_user(self.user)
        self.client.post(
            self.base_url, {"title": "User List", "description": "Regular user's list"}
        )

        # Switch to admin user
        self.authenticate_user(self.admin_user)
        self.client.post(
            self.base_url, {"title": "Admin List", "description": "Admin user's list"}
        )

        # Act
        response = self.client.get(self.base_url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Should see both lists

    def test_user_can_only_see_own_lists(self):
        """Test that regular users can only see their own lists"""
        # Arrange
        # Create admin's list
        self.authenticate_user(self.admin_user)
        self.client.post(
            self.base_url, {"title": "Admin List", "description": "Admin user's list"}
        )

        # Switch to regular user
        self.authenticate_user(self.user)
        self.client.post(
            self.base_url, {"title": "User List", "description": "Regular user's list"}
        )

        # Act
        response = self.client.get(self.base_url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1  # Should only see their own list
        assert response.data[0]["title"] == "User List"
