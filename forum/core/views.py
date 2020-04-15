from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from api.models import Topic
from api.serializers import TopicSerializer
from core.models import UserNotification
from core.serializers import UserNotificationSerializer


class MostPopularTopicsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):  # noqa
        queryset = Topic.get_most_popupar_topics()
        serializer = TopicSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class UserNotificationListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    queryset = UserNotification.objects.all()
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class UserNotificationDestroyView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    queryset = UserNotification.objects.all()

