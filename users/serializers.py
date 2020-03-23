from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username",
                  "password",
                  "avatar",
                  "gender",
                  "email",
                  "game_nickname"]


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["avatar",
                  "username",
                  "popularity",
                  "blood_coins",
                  "gender",
                  "game_nickname",
                  "birth_date",
                  "violations",
                  "description",
                  "email",
                  "pk"]


class RestrictedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["avatar",
                  "username",
                  "popularity",
                  "gender",
                  "game_nickname",
                  "violations",
                  "description",
                  "email"]