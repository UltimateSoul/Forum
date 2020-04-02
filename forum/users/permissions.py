from rest_framework import permissions

from users.models import Team


class IsTeamOwnerRankPermission(permissions.BasePermission):
    message = 'Only team owners could manage ranks.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        team_id = request.data.get('team')
        if user.is_authenticated and team_id:
            try:
                team = Team.objects.get(id=team_id)
                return team.owner == user
            except Team.DoesNotExist:
                print("Team doesn't exist")
        return False
