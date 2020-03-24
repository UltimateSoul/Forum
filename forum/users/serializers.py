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


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["avatar",
                  "gender",
                  "game_nickname",
                  "birth_date",
                  "description",
                  "email"]

    def validate_avatar(self, image):
        mb3 = 3145728
        if image.size > mb3:
            assert serializers.ValidationError(f"Your image size must be less than 3 mb")
        return image

    def validate_birth_date(self, date):
        return date


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