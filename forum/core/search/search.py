from core.documents import TopicDocument
from elasticsearch_dsl.query import Q


def search_for_movie_title(search_string: str, section: str) -> list:
    """
    Searches for suggestion by given string via elasticsearch
    :param search_string:
    :return: list of strings
    """
    topics = TopicDocument.search()
    topics = topics.query(Q('bool',
                            must=[Q("match", section=section),
                                  Q("fuzzy", title=search_string)]))
    topics = topics.execute()
    suggestions = [{'text': topic.title,
                    'id': topic.id} for topic in topics]
    if not suggestions:
        topics = TopicDocument.search().suggest('auto_complete',
                                                search_string,
                                                completion={'field': 'title.suggest',
                                                            'fuzzy': True})
        topics = topics.execute()
        suggestions = topics.suggest.auto_complete[0]['options']
        suggestions = [{'text': suggestion['text'],
                        'id': suggestion['_source']['id']} for suggestion in suggestions]
    return suggestions