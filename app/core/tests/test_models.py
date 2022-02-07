import email
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModerTest(TestCase):
    def test_create_user_with_email_succesful(self):
        """Test creating a new user with an email is succesful"""
        email = 'testname@somedomain.com'
        password = 'TestPasword320942'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))