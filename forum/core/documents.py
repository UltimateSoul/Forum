from django_elasticsearch_dsl import fields, Index
from django_elasticsearch_dsl.documents import Document
from elasticsearch_dsl import analyzer, tokenizer
from api.models import Topic


movie_index = Index('topics')
movie_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

basic_analyzer = analyzer('basic_analyzer',
                          tokenizer=tokenizer(
                              'trigram',
                              'edge_ngram',
                              min_gram=1,
                              max_gram=20
                          ),
                          filter=['lowercase'])


@movie_index.doc_type
class TopicDocument(Document):

    id = fields.IntegerField(
        attr='id'
    )

    title = fields.TextField(
        attr='title',
        fields={
            'suggest': fields.Completion(
                analyzer=basic_analyzer,
            ),
        }
    )

    class Django:
        model = Topic
