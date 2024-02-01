from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

BASE_USERS_URL = reverse("users:register")


class UsersRegistrationAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_email_required(self):
        res = self.client.post(
            BASE_USERS_URL,
            {
                "email": "",
                "password": "<PASSWORD>",
                "first_name": "John",
                "last_name": "Doe",
            },
        )

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        data = get_user_model().objects.all()
        self.assertEqual(len(data), 0)

    def test_registration_user(self):
        res = self.client.post(
            BASE_USERS_URL,
            {
                "email": "test@test.com",
                "password": "<PASSWORD>",
                "first_name": "John",
                "last_name": "Doe",
            },
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        data = get_user_model().objects.all()
        self.assertEqual(len(data), 1)
