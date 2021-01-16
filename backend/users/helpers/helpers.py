
def user_directory_path(self, filename):
    return f'avatars/users/{self.id}/{filename}'


def team_directory_path(self, filename):
    return f'avatars/teams/{self.name}/{filename}'