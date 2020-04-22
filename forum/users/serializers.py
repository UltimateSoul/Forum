from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Team, TeamMember, Rank, UserTeamRequest

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
    has_team = serializers.ReadOnlyField()
    team_id = serializers.SerializerMethodField()
    is_team_owner = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["avatar",
                  "username",
                  "popularity",
                  "coins",
                  "gender",
                  "game_nickname",
                  "date_joined",
                  "birth_date",
                  "violations",
                  "description",
                  "email",
                  "is_moderator",
                  "has_team",
                  "team_id",
                  "is_team_owner",
                  "pk"]

    def get_team_id(self, user):
        team = user.get_team()
        return team.id if team else None

    def get_is_team_owner(self, user):
        try:
            user.my_team
        except Team.DoesNotExist:
            return False
        return True


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
    owner = UserSerializer(required=False)
    members = TeamMemberRestrictedSerializer(read_only=True, many=True)

    def update(self, instance, validated_data):
        if validated_data.get('avatar') and instance.avatar:
            instance.avatar.delete()  # needs to not save redundant images on server
        for field_name, value in validated_data.items():
            setattr(instance, field_name, value)
        instance.save()
        return instance

    def validate_avatar(self, image):
        mb3 = 3145728
        if image.size > mb3:
            assert serializers.ValidationError("Your image size must be less than 3 mb")
        return image

    class Meta:
        model = Team
        fields = '__all__'


class UserTeamRequestSerializer(serializers.ModelSerializer):
    user = RestrictedUserSerializer(required=False)
    team = TeamSerializer()

    class Meta:
        model = UserTeamRequest
        fields = '__all__'


class CreateUserTeamRequestSerializer(serializers.ModelSerializer):
    user = RestrictedUserSerializer(required=False)

    def save(self, **kwargs):
        user = self.context.get('request').user
        team_id = self.data.get('team')
        request, is_created = UserTeamRequest.objects.get_or_create(user=user, team_id=team_id)
        if not is_created:
            request.approved = False  # Need to guarantee that even if previously user was accepted or rejected,
            request.email_was_send = False  # his current state was changed
            request.save()
        return request, is_created

    class Meta:
        model = UserTeamRequest
        fields = '__all__'
