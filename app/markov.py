import re
from typing import Generator

from config import Config
from model import (
    TextGenerator, PostgresStorage, EncoderStorage, ChainStorage)


__encoder_storage: EncoderStorage = None
__chain_storage: ChainStorage = None
__model: TextGenerator = None


def get_model() -> TextGenerator:
    global __model
    return __model


def set_model(model: TextGenerator) -> None:
    global __model
    __model = model


def get_encoder_storage() -> EncoderStorage:
    global __encoder_storage
    if not __encoder_storage:
        __encoder_storage = EncoderStorage.connect(
            host=Config.PG_HOST,
            port=Config.PG_PORT,
            user=Config.PG_USER,
            password=Config.PG_PASS,
            dbname=Config.PG_DBNAME)
    return __encoder_storage


def get_chain_storage() -> ChainStorage:
    global __chain_storage
    if not __chain_storage:
        __chain_storage = ChainStorage.connect(
            host=Config.PG_HOST,
            port=Config.PG_PORT,
            user=Config.PG_USER,
            password=Config.PG_PASS,
            dbname=Config.PG_DBNAME)
    return __chain_storage


def get_postgres_storage(request_dict: dict) -> PostgresStorage:
    pg_host = request_dict.get('pg_host')
    pg_port = request_dict.get('pg_port')
    pg_dbname = request_dict.get('pg_dbname')
    pg_user = request_dict.get('pg_user')
    pg_password = request_dict.get('pg_password')
    return PostgresStorage.connect(
        host=pg_host, port=pg_port, dbname=pg_dbname, user=pg_user, password=pg_password)


def parse_query(query: str) -> tuple:
    query = re.sub(r'[^\w,.=><\'" ]', '', query)
    params = [param[1:-1] for param in re.findall(r'"(.*?)"', query)]
    query = re.sub(r'"(.*?)"', '%s', query)
    return query, params


def get_text_corpus_from_postgres(request_dict: dict) -> Generator:
    pg_storage = get_postgres_storage(request_dict)
    query, params = parse_query(request_dict.get('sql_query'))
    print(query, query.find("'"))
    return (gen for gen in (pg_storage.exec_query(query, params),))


def get_text_corpus_from_file(request) -> Generator:
    file = request.files['train_file']
    separator = request.form.get('text_separator')
    return (text for text in file.read().decode('utf-8').split(separator))
