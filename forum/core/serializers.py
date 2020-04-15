from rest_framework import serializers

from core.models import UserNotification


class SuggestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()


class UserNotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserNotification
        fields = '__all__'
