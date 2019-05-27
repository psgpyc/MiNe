from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """serializer for user"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'phone_number')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create a new user a encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)
