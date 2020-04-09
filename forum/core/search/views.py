from rest_framework.response import Response
from rest_framework.views import APIView

from core.search.search import search_for_movie_title
from core.serializers import SuggestionsSerializer


class SearchTopics(APIView):

    def get(self, request, *args, **kwargs):  # noqa
        query = self.request.GET.get('query')
        suggestions = search_for_movie_title(query)
        serializer = SuggestionsSerializer({'suggestions': suggestions})
        return Response(data=serializer.data)