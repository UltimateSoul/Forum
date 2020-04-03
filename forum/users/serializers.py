from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Team, TeamMember, Rank

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
                  "game_nickname",
                  "violations",
                  "description"]


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["avatar",
                  "gender",
                  "game_nickname",
                  "description",
                  "birth_date",
                  "email"]

    def validate_avatar(self, image):
        mb3 = 3145728
        if image.size > mb3:
            assert serializers.ValidationError("Your image size must be less than 3 mb")
        return image


class TeamMembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeamMember
        fields = '__all__'


class RankRestrictedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = ['name']


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'


class TeamMemberRestrictedSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    rank = RankRestrictedSerializer(read_only=True)

    class Meta:
        model = TeamMember
        fields = ['user', 'team', 'rank', 'joined_at']


class TeamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    total_members = serializers.ReadOnlyField()
    owner = UserSerializer()
    members = TeamMemberRestrictedSerializer(read_only=True, many=True)

    class Meta:
        model = Team
        fields = '__all__'