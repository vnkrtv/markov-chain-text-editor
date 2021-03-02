import re
from typing import Generator, Optional, List

from markov import NgrammTextGenerator
from markov.utils import PostgresStorage

__model: Optional[NgrammTextGenerator] = None


def get_model() -> NgrammTextGenerator:
    global __model
    return __model


def set_model(model: NgrammTextGenerator) -> None:
    global __model
    __model = model


def parse_query(query: str) -> tuple:
    params = list(re.findall(r"'(.*?)'", query))
    query = re.sub(r"'(.*?)'", '%s', query)
    return query, params


def get_postgres_storage(request_dict: dict) -> PostgresStorage:
    pg_host = request_dict.get('pg_host')
    pg_port = request_dict.get('pg_port')
    pg_dbname = request_dict.get('pg_dbname')
    pg_user = request_dict.get('pg_user')
    pg_password = request_dict.get('pg_password')
    return PostgresStorage.connect(
        host=pg_host, port=pg_port, dbname=pg_dbname, user=pg_user, password=pg_password)


def get_text_corpus_from_postgres(request_dict: dict) -> Generator:
    pg_storage = get_postgres_storage(request_dict)
    query, params = parse_query(request_dict.get('sql_query'))
    return (row[0] for row in pg_storage.exec_query(query, params))


def get_text_corpus_from_file(request) -> Generator:
    file = request.files['train_file']
    separator = request.form.get('text_separator')
    return (text for text in file.read().decode('utf-8').split(separator))


class RequestStack:
    stack: List[dict]
    locked: bool

    def __init__(self):
        self.stack = []
        self.locked = False

    def push(self, msg: dict):
        self.stack.append(msg)

    def pop(self) -> dict:
        return self.stack.pop()

    def clear(self):
        self.stack = []

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False


__msg_stack: Optional[RequestStack] = RequestStack()


def get_msg_stack() -> RequestStack:
    global __msg_stack
    return __msg_stack
