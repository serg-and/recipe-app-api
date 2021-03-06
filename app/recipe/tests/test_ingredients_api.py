from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsApiTests(TestCase):
    """Test the public ingredients API"""
    def setUp(self):
        self.client = APIClient()
    
    def test_login_required(self):
        """Test that login is required for retrieving ingredients"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Teset the public ingredients API"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'testsu@somedomain.com',
            'TestSUPasword3342942'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tst_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredient.objects.create(user=self.user, name='sla')
        Ingredient.objects.create(user=self.user, name='ijs')

        res = self.client.get(INGREDIENTS_URL)

        ingredient = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredient, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_ingredients_limited_to_user(self):
        """Test that ingredients returned are only from the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@somedomain.com',
            'otherTestSUPasword3342942'
        )
        Ingredient.objects.create(user=user2, name='Sla')
        ingredient = Ingredient.objects.create(user=self.user, name='Ijs')
        res = self.client.get(INGREDIENTS_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_succesful(self):
        """Test creating a new ingredient"""
        payload = {'name': 'Test ingredient'}
        self.client.post(INGREDIENTS_URL, payload)
        
        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)
    
    def test_create_ingredient_invalid(self):
        """Test creating a new ingredient with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
