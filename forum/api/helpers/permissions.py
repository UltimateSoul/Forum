

def check_ability_to_edit(user, obj):
    """Works with posts/comments/topics and minichat messages"""
    return user.id == obj.author.id or user.is_staff or user.is_superuser

def check_ability_to_delete(user):
    """Only admins can delete objects"""
    return user.is_staff or user.is_superuser
