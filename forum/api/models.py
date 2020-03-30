from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


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
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to='static/images/icons', blank=True,
                             null=True)
    description = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='topics')
    section = models.CharField(max_length=13, choices=SECTION_CHOICES,
                               default=CONVERSATION)
    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return f"sections/{self.section}/{self.id}-1/"

    @property
    def posts_quantity(self):
        return Post.objects.filter(topic=self).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-created_date']


class MiniChatMessage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() > 1000:
            self.objects.first().delete()
        super(MiniChatMessage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Mini-Chat Message'
        verbose_name_plural = 'Mini-Chat Messages'
        ordering = ['-created_date']


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return ' '.join(self.body.split()[:4])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['published_date']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    likes = GenericRelation(Like)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.body[:10]

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['published_date']
