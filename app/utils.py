import re
from typing import Generator, Iterable, Optional, List, Tuple, Dict, Any

from config import Config
from engine.markov import PostgresStorage
from engine.elastic import ElasticEngine

__es: ElasticEngine = ElasticEngine.connect(
    host=Config.ELASTIC_HOST,
    port=Config.ELASTIC_PORT,
    user=Config.ELASTIC_USER,
    password=Config.ELASTIC_PASS)


def get_elastic_engine() -> ElasticEngine:
    global __es
    return __es


def parse_query(query: str) -> Tuple[str, List[str]]:
    params = list(re.findall(r"'(.*?)'", query))
    query = re.sub(r"'(.*?)'", '%s', query)
    return query, params


def get_postgres_storage(request_dict: Dict[str, Any]) -> PostgresStorage:
    pg_host = request_dict.get('pg_host')
    pg_port = request_dict.get('pg_port')
    pg_dbname = request_dict.get('pg_dbname')
    pg_user = request_dict.get('pg_user')
    pg_password = request_dict.get('pg_password')
    return PostgresStorage.connect(
        host=pg_host, port=pg_port, dbname=pg_dbname, user=pg_user, password=pg_password)


def get_text_corpus_from_postgres(request_dict: Dict[str, Any]) -> Iterable[str]:
    pg_storage = get_postgres_storage(request_dict)
    query, params = parse_query(request_dict.get('sql_query'))
    return (row[0] for row in pg_storage.exec_query(query, params))


def get_text_corpus_from_file(request) -> Iterable[str]:
    file = request.files['train_file']
    separator = request.form.get('text_separator')
    return (text for text in file.read().decode('utf-8').split(separator))
