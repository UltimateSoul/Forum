import factory

from api.models import Topic, Post, Comment, Tag


class TopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Topic

    title = 'Test Title'
    body = 'Test body'
    description = 'Test description'
    section = Topic.CONVERSATION


class TagFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Tag

    name = 'test tag'


class PostFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Post
    body = 'Test Post'


class CommentFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Comment
    body = 'Test Comment'

