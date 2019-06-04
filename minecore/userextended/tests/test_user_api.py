from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('userextended:create-user')
TOKEN_URL = reverse('userextended:token-user')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email': "nepal@gmail.com",
            'password': 'helloworld123',
            'phone_number': '9802151714',
            'name': 'mr.ghimire',
            }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Tests creating user that already exists fails"""

        payload = {
            'email': 'nepal@gmail.com',
            'password': 'nepal123',
            'name': 'psg',
            'phone_number': '9802051714'
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password is more than 5 character long"""
        payload = {
            'email': 'paritosh.ghimire666@gmail.com',
            'password': 'npp',
            'name': 'psg',
            'phone_number': '9802051714'}
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_user(self):
        """Test token is created for user"""
        payload = {
            'email': 'paritosh.ghimire666@gmail.com',
            'password': 'npp',
            'name': 'psg',
            'phone_number': '9802051714'}
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test token is not created if invalid credentials are given"""
        create_user(
            email="psg@gmail.com",
            password="helpme123",
            name="psg",
            phone_number="9802051714")
        payload = {
            'email': "psg@gmail.com",
            'password': 'helpmw12'}

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesnot exists"""
        payload = {
            'email': 'paritosh.ghimire666@gmail.com',
            'password': 'npp',
            'name': 'psg',
            'phone_number': '9802051714'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {
            'email': 'paritosh.ghimire666@gmail.com',
            'password': 'npp',
            'name': '',
            'phone_number': '9802051714'}
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
