from rest_framework import generics
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UserSerializer
