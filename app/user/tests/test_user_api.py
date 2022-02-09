import email
from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public users API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_valid_user_succes(self):
        """Test create user with payload is valid"""
        payload = {
            'email': 'username@adress.com',
            'password': 'userPassword',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
    
    def test_user_exists(self):
        """Test if creating a user that already exits fails"""
        payload = {
            'email': 'sadfsaf@adress.com',
            'password': 'ljoieijasoijndi',
            'name': 'tst',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short(self):
        """Test that creating a user with a password with 5 or less characters fails"""
        payload = {
            'email': 'adsfefe@adress.com',
            'password': 'pwd',
            'name': 'tst',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email']).exists()
        self.assertFalse(user_exists)
    
    # # TODO: FIX test failing
    # def test_create_token_for_user(self):
    #     """Test that a token is created for the user"""
    #     payload = {
    #         'email': 'test@londonappdev.com',
    #         'password': 'testpass',
    #     }
    #     create_user(**payload)
    #     res = self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token', res.data)
    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        payload = {
            'email': 'sadfsaf@adress.com',
            'password': 'ljoieijasoijndi',
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, {
            'email': payload['email'],
            'password': 'invalid_password0979845',
        })

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {
            'email': 'sadfsaf@adress.com',
            'password': 'ljoieijasoijndi',
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {
            'email': 'saddffsaf@adress.com',
            'password': '',
        })
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    

class PrivateUserApiTests(TestCase):
    def setUp(self):
        self.user = create_user(
            email='someuser@somedomain.com',
            password='somepassword',
            name='somename'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })
    
    def test_post_to_me_not_allowed(self):
        """Test that posting to the me url is not allowed"""
        res = self.client.post(ME_URL, {})
        
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_user_update_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {
            'name': 'new name',
            'password': 'newpassword304823975',
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
