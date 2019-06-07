from rest_framework import serializers

from coremodels import models


class TagSerializer (serializers.ModelSerializer):
    """Serializer for tag serializer"""
    class Meta:
        model = models.Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
