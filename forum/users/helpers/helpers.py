
def user_directory_path(self, filename):
    return f'avatars/user_{self.id}/{filename}'


def team_directory_path(self, filename):
    return f'avatars/team_{self.id}/{filename}'


def search_team_for_user(user):
    team = user.my_team
    if team:
        return team
    team = user.teammembership.team
    if team:
        return team