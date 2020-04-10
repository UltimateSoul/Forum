from rest_framework.response import Response
from rest_framework.views import APIView

from core.search.search import search_for_movie_title
from core.serializers import SuggestionsSerializer


class SearchTopics(APIView):

    def get(self, request, *args, **kwargs):  # noqa
        query = self.request.GET.get('query')
        section = self.request.GET.get('section')
        suggestions = search_for_movie_title(query, section)
        serializer = SuggestionsSerializer({'suggestions': suggestions})
        return Response(data=serializer.data)