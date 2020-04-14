from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Topic
from api.serializers import TopicSerializer


class MostPopularTopicsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):  # noqa
        queryset = Topic.get_most_popupar_topics()
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
