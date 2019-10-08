from django.conf import settings
from django.db import models

# Create your models here.


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
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='topic')
    description = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='topics')
    rating = models.IntegerField(default=0)
    section = models.CharField(max_length=13, choices=SECTION_CHOICES,
                               default=CONVERSATION)

    def get_absolute_url(self):
        return f"sections/{self.section}/{self.id}-1/"

    @property
    def posts_quantity(self):
        return Post.objects.filter(topic=self).count()

    def __str__(self):
        return self.title


class MiniChatMessage(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count() > 100:
            self.objects.first().delete()
        super(MiniChatMessage, self).save(*args, **kwargs)


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE,
                              related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    rating = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)
    edited_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ' '.join(self.body.split()[:4])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    rating = models.IntegerField(default=0)
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:10]
