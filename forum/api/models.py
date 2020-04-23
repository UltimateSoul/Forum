import datetime

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.models import ModeratorLog


class Like(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __rerp__(self):
        return f'Like(user={self.user})'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
        ordering = ['-created_at']


class Topic(models.Model):
    IDEAS = 'IDEAS'
    CONVERSATION = 'CONVERSATION'
    BUGS = 'BUGS'
    ENTERTAINMENT = 'ENTERTAINMENT'
    SHOP = 'SHOP'
    SECTION_CHOICES = (
        (IDEAS, 'Ideas'),
        (CONVERSATION, 'Conversation'),
        (BUGS, 'Bugs'),
        (ENTERTAINMENT, 'Entertainment'),
        (SHOP, 'Shop'),
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField()
    description = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='topics')
    section = models.CharField(max_length=13, choices=SECTION_CHOICES, default=CONVERSATION)

    removed_by_moderator = models.BooleanField(default=False)
    removed_at = models.DateTimeField(null=True, blank=True)

    is_pinned = models.BooleanField(default=False)
    likes = GenericRelation(Like)

    tags = models.ManyToManyField("Tag", related_name='topic')

    def total_likes(self):
        return self.likes.count()

    @property
    def posts_quantity(self):
        return Post.objects.filter(topic=self).count()

    def __str__(self):
        return self.title

    @classmethod
    def get_most_popupar_topics(cls):
        now = datetime.datetime.now()
        week_ago = now - datetime.timedelta(days=7)
        last_week_topics = cls.objects.filter(edited_at__range=(week_ago, now))
        filtered_topics = list(filter(lambda topic: topic.total_likes() * topic.posts_quantity, last_week_topics))
        return filtered_topics[4::-1]

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-edited_at']


class MiniChatMessage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):  # noqa
        if self.__class__.objects.count() > 10000:
            to_delete_messages = self.__class__.objects.order_by('created_at')[:5000]
            self.__class__.objects.filter(id__in=to_delete_messages).delete()
        super(MiniChatMessage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Mini-Chat Message'
        verbose_name_plural = 'Mini-Chat Messages'
        ordering = ['-created_at']


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return ' '.join(self.body.split()[:4])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.body[:10]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_at']


class Tag(models.Model):

    name = models.CharField(max_length=255)

    def __repr__(self):
        return f'Tag - {self.name}'
