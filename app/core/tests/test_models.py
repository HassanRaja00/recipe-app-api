from django.test import TestCase
from django.contrib.auth import get_user_model  # better for large cb
from unittest.mock import patch

from core import models


def sample_user(email='test@test.com', password='test123'):
    '''Create sample user'''
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        '''Test creating user with new email is successful'''
        email = '123@123.com'
        password = '123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # since password is encrypted
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        '''Test the email if new user email is normalized'''
        email = '123@TEST.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        '''Test creating user with no email raises error'''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        '''Test creating new superuser'''
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        '''Test tag string representation'''
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        '''Test ingredient string representation'''
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Apple'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        '''Test recipe string representation'''
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Test Recipe',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        '''Img saved is in the correct location'''
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, 'myimg.jpg')

        expected_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, expected_path)
