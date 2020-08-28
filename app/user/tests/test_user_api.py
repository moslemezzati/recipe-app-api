from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.clinet = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'Test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test creating user that already exists fails"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 charactre"""
        payload = {'email': 'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'moslem@gmail.com', 'password': '123456789'}
        create_user(**payload)
        res = self.clinet.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_for_invalid_creadentials(self):
        """Test that token is not generated if invalid credenatials are given"""
        create_user(email='moslem@gamil.com', password='testpass')
        payload = {'email': 'moslem@gmail.com', 'password': 'pw'}
        res = self.clinet.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user dosen't exist"""
        payload = {'email': 'moslem@gmail.com', 'password': 'testpass'}
        res = self.clinet.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)        

    def test_create_token_missing_fields(self):
        """Test that email and passwrod are required"""
        payload = {'email': 'com', 'password': ''}
        res = self.clinet.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

