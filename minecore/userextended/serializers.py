from django.contrib.auth import get_user_model, authenticate

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


class AuthTokenSerializer(serializers.Serializer):
    """serializer for the user authentication object"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password)
        if not user:
            message = 'Unable to Authenticate with provided credentials'
            raise serializers.ValidationError(message, code='authentication')

        attrs['user'] = user
        return attrs
