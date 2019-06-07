from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from coremodels.models import Tag

from .. import serializers

TAG_URL = reverse('products:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for accessing a tag
        and user need to be superuser"""

        response = self.client.get(TAG_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test that only authorised user has access to tags"""

    def setUp(self):
        self.user = get_user_model().objects.create_staff(
            email="psg@gmail.com",
            password="myepicpassword"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name="cotton")
        Tag.objects.create(user=self.user, name="allo")

        response = self.client.get(TAG_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = serializers.TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
