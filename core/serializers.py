from rest_framework import serializers

from users.serializers import UserSerializer
from . import models


class TopicSerializer(serializers.ModelSerializer):
    """Topic Serializer"""
    author = UserSerializer()

    class Meta:
        model = models.Topic
        fields = '__all__'

