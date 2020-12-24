import os

from dotenv import load_dotenv
from googlesearch import search
from elasticsearch import Elasticsearch

load_dotenv()
ELASTIC_NODES = os.getenv('ELASTIC_NODES')

ELASTICSEARCH_CLIENT = Elasticsearch([ipport for ipport in ELASTIC_NODES.split(",")])


def get_top5_google_result(query):
    query_search = ' '.join(query).lower()
    es = ElasSearch()
    es.create_document(query_search)
    return search(query_search, num_results=5)


def recent_search_result(query):
    query_search = ' '.join(query).lower()
    es = ElasSearch()
    return es.get_recent_search(query_search)


def search_query(query):
    return dict(query=dict(regexp=dict(document=dict(value=f".*{query}.*", flags="ALL",
                                                     max_determinized_states=10000, rewrite="constant_score"))))


class ElasSearch:

    def __init__(self):
        self.index = "recent_search"
        self.es = ELASTICSEARCH_CLIENT
        self.es.indices.create(index=self.index, ignore=400)

    def create_document(self, document):
        dic = {
            'document': document
        }
        if not self.es.exists(index=self.index, id=document):
            self.es.create(index=self.index, id=document, body=dic)

    def get_recent_search(self, query):
        query_es = search_query(query)
        results = self.es.search(index=self.index, body=query_es, size=100)
        recent_search = []
        if results.get('hits') and results['hits'].get('hits'):
            for result in results['hits']['hits']:
                recent_search.append(result['_source']['document'])
        return recent_search

