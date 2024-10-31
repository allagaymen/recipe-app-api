"""
Test for models .

"""
from decimal import Decimal
from core import models
from django.test import TestCase
from django.contrib.auth import get_user_model


def create_user(email='test@example.com', password="test123"):
    "create and return a new user."
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ test creating user with an email successfully."""
        email = 'test@example.com'
        password ='testpass1234'
        user = get_user_model().objects.create_user(
            email = email,
            password = password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """ Test email is normalized for new users ."""

        sample_email = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_email:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_errors(self):
        """Test creating new user without an email raises a ValueError. """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating superuser."""
        User = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(User.is_superuser)
        self.assertTrue(User.is_staff)
    
    def test_create_recipe(self):
        """Test creating a recipe is successful."""
        user = get_user_model().objects.create_user(
            'test@est.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title = 'Sample Recipe name',
            time_minutes = 5,
            price=Decimal('5.50'),
        )
        self.assertEqual(str(recipe),recipe.title)
    
    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='tag1')

        self.assertEqual(str(tag),tag.name)
    
    def test_create_ingredient(self):
        """Test creating a ingrediant is successful."""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user, 
            name='ingeridant 1'
            )

        self.assertEqual(str(ingredient),ingredient.name)
