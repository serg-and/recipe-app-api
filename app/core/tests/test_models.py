import email
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
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
    
    def test_new_user_email_normalized(self):
        """Test if the email is normalized for a new user"""
        email = 'testname@SomeDomain.com'
        user = get_user_model().objects.create_user(
            email=email
        )

        self.assertEqual(user.email, email.lower())
    
    def test_new_user_invalid_email(self):
        """Test if creating a user without email raises an error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testinpPassword')
    
    def test_create_superuser_succesfull(self):
        """Test creating a new superuser"""
        email = 'testsu@somedomain.com'
        password = 'TestSUPasword320942'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
