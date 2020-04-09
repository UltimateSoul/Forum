from rest_framework import serializers


class SuggestionsSerializer(serializers.Serializer):

    suggestions = serializers.ListField(child=serializers.CharField(max_length=255))