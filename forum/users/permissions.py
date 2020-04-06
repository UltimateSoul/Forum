from rest_framework import permissions

from users.models import Team, Rank, UserTeamRequest


class IsTeamOwnerRankPermission(permissions.BasePermission):
    message = 'Only team owners could manage ranks.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        try:
            team = user.my_team
            rank = Rank.objects.get(id=view.kwargs.get('pk'))
            return team == rank.team
        except Team.DoesNotExist:
            print("Team doesn't exist")
        return False


class IsTeamOwner(permissions.BasePermission):
    message = 'Only team owner could do this.'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            try:
                team = request.user.my_team
                if request.GET.get('teamID'):
                    return team.id == int(request.GET.get('teamID'))
            except (Team.DoesNotExist, ValueError):
                print("Team doesn't exist")
            return False
        elif request.method in ('PATCH', 'PUT', 'DELETE'):
            try:
                team = request.user.my_team
                user_request_team = UserTeamRequest.objects.get(id=view.kwargs.get('pk')).team
                return team == user_request_team
            except Team.DoesNotExist:
                print("Team doesn't exist")
            return False
        return True
