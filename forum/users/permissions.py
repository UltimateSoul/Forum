from rest_framework import permissions

from users.models import Team, Rank


class IsTeamOwnerRankPermission(permissions.BasePermission):
    message = 'Only team owners could manage ranks.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if user.is_authenticated:
            try:
                team = request.user.my_team
                rank = Rank.objects.get(id=view.kwargs.get('pk'))
                return team == rank.team
            except Team.DoesNotExist:
                print("Team doesn't exist")
        return False
