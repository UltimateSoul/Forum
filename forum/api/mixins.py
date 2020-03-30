from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api import services
from api.serializers import FanSerializer
from api.helpers import status as tbw_status

class LikedMixin:

    def get_object(self):
        raise NotImplementedError('Not implemented')

    @action(methods=['POST'], detail=True)
    def like(self, request, **kwargs):
        """Add like to object"""
        obj = self.get_object()
        _, is_created = services.add_like(obj, request.user)
        if is_created:
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=tbw_status.STATUS_220_ALREADY_LIKED)

    @action(methods=['POST'], detail=True)
    def unlike(self, request, **kwargs):
        """Delete like from object"""
        obj = self.get_object()
        services.remove_like(obj, request.user)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['GET'], detail=True)
    def fans(self, request, **kwargs):
        """Get all users which liked object"""
        obj = self.get_object()
        fans = services.get_fans(obj)
        serializer = FanSerializer(fans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
