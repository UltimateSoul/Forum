from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import Like
User = get_user_model()


def add_like(obj, user: User) -> tuple:
    """Add like to object"""
    obj_type = ContentType.objects.get_for_model(obj)
    like, is_created = Like.objects.get_or_create(
        content_type=obj_type, object_id=obj.id, user=user)
    return like, is_created


def remove_like(obj, user):
    """Delete like from object"""
    obj_type = ContentType.objects.get_for_model(obj)
    Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user
    ).delete()


def is_liked(obj, user) -> bool:
    """Checks if user have already liked object or not"""
    if not user.is_authenticated:
        return False
    obj_type = ContentType.objects.get_for_model(obj)
    likes = Like.objects.filter(
        content_type=obj_type, object_id=obj.id, user=user)
    return likes.exists()


def get_fans(obj):
    """Get all users which liked object"""
    obj_type = ContentType.objects.get_for_model(obj)
    return User.objects.filter(
        likes__content_type=obj_type, likes__object_id=obj.id)
