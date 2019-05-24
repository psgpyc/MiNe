from django.test import (
    TestCase,
    Client,)
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError


class AdminSiteTests(TestCase):
    def setUp(self):
        """Setup is run before every tests.
        Client and SuperUser Creation for every test functions."""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="paritosh.ghimire666@gmail.com",
            password="nepal123",)
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="paritosh.ghimire@gmail.com",
            password="nepal123",
            phone_number="9802051714",
            name="paritosh sharma ghimire",)

    def test_user_are_listed(self):
        """Check users are listed in Django admin page"""
        url = reverse("admin:core_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name) # It also checks HTTP response is 200
        self.assertContains(response, self.user.email)

    def test_user_change_page(self):
        """Test that user update page works"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)












