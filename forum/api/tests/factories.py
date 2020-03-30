import factory

from api.models import Topic, Post, Comment


class TopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Topic

    title = 'Test Title'
    body = 'Test body'
    description = 'Test description'
    section = Topic.CONVERSATION


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post
    body = 'Test Post'


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment
    body = 'Test Comment'

