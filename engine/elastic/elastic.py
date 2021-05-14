import uuid
from typing import List, Union, Optional, Dict, Any, Iterable

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError


class ElasticEngine:
    es: Elasticsearch
    bulk_actions_count: int = 10_000

    def __init__(self, es: Elasticsearch):
        self.es = es

    @classmethod
    def connect(cls, host: str, port: Union[int, str], user: Optional[str], password: Optional[str]):
        con_str = f'http://{user}:{password}@{host}:{port}/' if user and password else f'{host}:{port}'
        es = Elasticsearch(con_str)
        if not es.ping():
            raise ConnectionError('ping failed')
        return cls(es)

    def add_index(self, name: str, number_of_shards: int = 1, number_of_replicas: int = 2) -> None:
        self.es.indices.create(index=name, body={
            "settings": {
                "index": {
                    "number_of_shards": number_of_shards,
                    "number_of_replicas": number_of_replicas,
                    "analysis": {
                        "analyzer": {
                            "t9_analyzer": {
                                "type": "custom",
                                "tokenizer": "standard",
                                "filter": [
                                    "lowercase",
                                    "custom_edge_ngram"
                                ]
                            }
                        },
                        "filter": {
                            "custom_edge_ngram": {
                                "type": "edge_ngram",
                                "min_gram": 2,
                                "max_gram": 10
                            }
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "text": {
                        "type": "text",
                        "analyzer": "t9_analyzer",
                        "search_analyzer": "standard"
                    }
                }
            }
        })

    def add_doc(self, index_name: str, text: str) -> None:
        self.es.index(index=index_name, body={
            'text': text
        })

    def add_many(self, index_name: str, sentences: Iterable, bulk_actions_count: int = 10_000) -> None:
        self.bulk_actions_count = bulk_actions_count
        actions = []
        for sentence in sentences:
            if len(actions) < self.bulk_actions_count:
                actions.append({
                    '_op_type': 'create',
                    '_index': index_name,
                    '_id': uuid.uuid4(),
                    'text': sentence
                })
            else:
                helpers.bulk(self.es, actions=actions, stats_only=True)
                actions = []
        else:
            helpers.bulk(self.es, actions=actions, stats_only=True)

    def delete_index(self, index_name: str) -> None:
        self.es.indices.delete(index=index_name)

    def get_indices_stats(self, index_name: str) -> Dict[str, Any]:
        return self.es.indices.stats(index=index_name, human=True).get("indices", {})

    def get(self, index_name: str, phrase: str, count: int = 10, phrase_len: int = 10) -> List[str]:
        sentences = [
            doc['_source']['text']
            for doc in self.es.search(
                index=index_name,
                body={
                    "query": {
                        "match_phrase": {
                            "text": phrase
                        }
                    },
                    "size": count
                })['hits']['hits']
        ]
        return [
            ' '.join(sentence[sentence.find(phrase):].split()[:phrase_len])
            for sentence in sentences
        ]
