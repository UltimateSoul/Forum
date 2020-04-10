from rest_framework import serializers


class SuggestionsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()