from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


from .models import Topic
from .serializers import TopicSerializer


class TopicView(APIView):
    """Topics"""

    def get(self, request):
        topics = Topic.objects.all()
        setializer = TopicSerializer(topics, many=True)
        return Response(setializer.data)


