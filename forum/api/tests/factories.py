import factory

from api.models import Topic


class TopicFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Topic

    title = 'Test Title'
    body = 'Test body'
    description = 'Test description'
    section = Topic.CONVERSATION
