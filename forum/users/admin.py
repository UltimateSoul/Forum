from django.contrib import admin

from .models import User, Team, Rank, TeamMember, UserTeamRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('game_nickname',
                    'email',
                    'popularity',
                    'blood_coins',
                    'date_joined')


class TeamMembersInline(admin.TabularInline):
    model = TeamMember


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):

    list_display = ('name', 'owner', 'members_count')
    inlines = [
        TeamMembersInline
    ]

    @staticmethod
    def members_count(obj):
        return obj.members.count()


@admin.register(Rank)
class RankAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_name')

    @staticmethod
    def team_name(obj):
        if obj.team:
            return obj.team.name
        return 'doesnt exist'


@admin.register(UserTeamRequest)
class UserTeamRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'team_name', 'approved', 'email_was_send')

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def team_name(obj):
        if obj.team:
            return obj.team.name
        return 'doesnt exist'

