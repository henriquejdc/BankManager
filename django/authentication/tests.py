# Base imports
from typing import List

# Django imports
from django.urls import reverse

# Third party imports
from rest_framework import status

# Project imports
from shared.tests import BaseAPITestCase


class HealthAuthView(BaseAPITestCase):
    """Test all scenarios for HealthAuthView."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("health_auth")

    def test_health_200(self):
        response = self.client.get(f'{self.url}')
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class UserCreateView(BaseAPITestCase):
    """Test all scenarios for HealthAuthView."""

    tests_to_perform: List = []

    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("sign_up")

    def test_signup_200(self):
        response = self.client.post(
            f'{self.url}', data={
                'username': 'test',
                'email': 'test@test.com',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_signup_400(self):
        response = self.client.post(
            f'{self.url}', data={
                'username': 'test',
                'password': 'test@test',
            }
        )
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
