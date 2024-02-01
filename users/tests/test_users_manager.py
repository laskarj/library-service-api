from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTests(TestCase):
    def test_create_superuser(self):
        User = get_user_model()
        email = "admin@example.com"
        password = "adminpassword"

        superuser = User.objects.create_superuser(email, password)

        self.assertIsInstance(superuser, User)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))
