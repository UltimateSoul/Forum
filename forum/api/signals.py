from datetime import datetime

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from api.models import Topic, Post, Comment


@receiver(pre_save, sender=Topic)
def update_topic_state(sender, instance=None, created=False, **kwargs):
    instance.edited_at = datetime.now()


@receiver(post_save, sender=Post)
def update_topic_edited_at_through_post(sender, instance=None, created=False, **kwargs):
    instance.topic.edited_at = datetime.now()
    instance.topic.save()


@receiver(post_save, sender=Comment)
def update_topic_edited_at_through_comment(sender, instance=None, created=False, **kwargs):
    instance.post.topic.edited_at = datetime.now()
    instance.post.topic.save()
