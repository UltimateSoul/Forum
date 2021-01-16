from rest_framework import serializers


class CoinsSerializer(serializers.Serializer):
    amount = serializers.IntegerField()