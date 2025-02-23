from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
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

    def get_list_payload(self):
        """Helper method to create a valid list payload"""
        list_obj = ListFactory.build(owner=None)
        return {"title": list_obj.title, "description": list_obj.description}

    @parameterized.expand(
        [
            (
                "missing_title",
                {"description": "Test description"},
                {
                    "type": "validation_error",
                    "errors": [
                        {
                            "code": "required",
                            "detail": "This field is required.",
                            "attr": "title",
                        }
                    ],
                },
            ),
            (
                "empty_title",
                {"title": "", "description": "Test description"},
                {
                    "type": "validation_error",
                    "errors": [
                        {
                            "code": "blank",
                            "detail": "This field may not be blank.",
                            "attr": "title",
                        }
                    ],
                },
            ),
            (
                "title_too_long",
                {"title": "x" * 101, "description": "Test description"},
                {
                    "type": "validation_error",
                    "errors": [
                        {
                            "code": "max_length",
                            "detail": "Ensure this field has no more than 100 characters.",
                            "attr": "title",
                        }
                    ],
                },
            ),
        ]
    )
    def test_list_creation_validation_errors(self, name, payload, expected_error):
        """Test validation errors when creating a list"""
        # Arrange
        self.authenticate_user(self.user)

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == expected_error

    @parameterized.expand(
        [
            ("authenticated_user", True),
            ("unauthenticated_user", False),
        ]
    )
    def test_list_creation_authentication(self, name, is_authenticated):
        """Test list creation with different authentication states"""
        # Arrange
        payload = self.get_list_payload()

        if is_authenticated:
            self.authenticate_user(self.user)
            expected_status = status.HTTP_201_CREATED
            expected_count = 1
        else:
            expected_status = status.HTTP_401_UNAUTHORIZED
            expected_count = 0

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == expected_status
        assert List.objects.count() == expected_count
        if is_authenticated:
            list_obj = List.objects.first()
            assert list_obj.title == payload["title"]
            assert list_obj.description == payload["description"]
            assert list_obj.owner == self.user

    @parameterized.expand(
        [
            ("admin_user", "admin_user", 2),
            ("regular_user", "user", 1),
        ]
    )
    def test_list_visibility(self, name, user_type, expected_count):
        """Test list visibility for different user types"""
        # Arrange
        user_list = ListFactory(owner=self.user)
        admin_list = ListFactory(owner=self.admin_user)

        # Set the appropriate user
        test_user = self.admin_user if user_type == "admin_user" else self.user
        self.authenticate_user(test_user)

        # Act
        response = self.client.get(self.base_url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == expected_count

        # Verify the correct lists are visible
        list_titles = {item["title"] for item in response.data}
        if user_type == "admin_user":
            assert user_list.title in list_titles
            assert admin_list.title in list_titles
        else:
            assert user_list.title in list_titles
            assert admin_list.title not in list_titles

    def test_successful_list_creation(self):
        """Test successful list creation with valid data"""
        # Arrange
        self.authenticate_user(self.user)
        payload = self.get_list_payload()

        # Act
        response = self.client.post(self.base_url, payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert List.objects.count() == 1
        list_obj = List.objects.first()
        assert list_obj.title == payload["title"]
        assert list_obj.description == payload["description"]
        assert list_obj.owner == self.user

        # Verify response structure
        assert "id" in response.data
        assert "created_at" in response.data
        assert "items" in response.data
        assert response.data["owner"] == self.user.username
