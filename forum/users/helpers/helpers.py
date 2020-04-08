
def user_directory_path(self, filename):
    return f'avatars/user_{self.id}/{filename}'


def team_directory_path(self, filename):
    return f'avatars/team_{self.id}/{filename}'