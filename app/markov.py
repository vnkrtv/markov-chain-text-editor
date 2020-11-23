import os
import re
from typing import Generator, Iterable

from config import BASE_DIR
from model import (
    PostgresStorage, WikiStorage, HabrStorage, EncoderStorage, ChainStorage)
from model import (
    MarkovModel, TextGenerator)
from model import (
    get_ram_model, get_db_model)

RAM_MODELS_LIST = os.listdir(os.path.join(BASE_DIR, 'model', 'bin'))
RAM_MODEL_NAME = RAM_MODELS_LIST[0] if RAM_MODELS_LIST else None
DB_MODEL_NAME = 'ngram'

__wiki_storage: WikiStorage = None
__habr_storage: HabrStorage = None
__encoder_storage: EncoderStorage = None
__chain_storage: ChainStorage = None
__model = None


def __get_wiki_storage(mongo_wiki_host: str) -> WikiStorage:
    global __wiki_storage
    if not __wiki_storage:
        __wiki_storage = WikiStorage.connect(
            host=mongo_wiki_host)
    return __wiki_storage


def __get_habr_storage(pg_habs_host: str) -> HabrStorage:
    global __habr_storage
    if not __habr_storage:
        __habr_storage = HabrStorage.connect(
            host=pg_habs_host, dbname='habr')
    return __habr_storage


def __get_encoder_storage(pg_encoder_host: str) -> EncoderStorage:
    global __encoder_storage
    if not __encoder_storage:
        __encoder_storage = EncoderStorage.connect(
            host=pg_encoder_host, dbname='markov')
    return __encoder_storage


def __get_chain_storage(pg_chain_host: str) -> ChainStorage:
    global __chain_storage
    if not __chain_storage:
        __chain_storage = ChainStorage.connect(
            host=pg_chain_host, dbname='markov')
    return __chain_storage


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
    query = re.sub(r'[^\w ]', '', request_dict.get('sql_query'))
    return (gen for gen in (pg_storage.exec_query(query),))


def get_text_corpus_from_file(request) -> Generator:
    file = request.files['train_file']
    separator = request.form.get('text_separator')
    return (text for text in file.read().decode('utf-8').split(separator))


def load_ram_model(model_name: str = None,
                   pg_habs_host: str = '172.17.0.3',
                   mongo_wiki_host: str = 'localhost') -> MarkovModel:
    global __model
    if not __model:
        if model_name:
            __model = MarkovModel.load(model_name)
        else:
            __model = get_ram_model(
                mongo_storage=__get_wiki_storage(mongo_wiki_host),
                postgres_storage=__get_habr_storage(pg_habs_host),
                model_state=3,
                wiki_articles_count=1000,
                habr_posts_count=1000
            )
            __model.save(model_name)
    return __model


def load_db_model(model_name: str = DB_MODEL_NAME,
                  train: bool = False,
                  train_corpus: Iterable = None,
                  pg_chain_host: str = '172.17.0.2',
                  pg_encoder_host: str = '172.17.0.2',
                  pg_habs_host: str = '172.17.0.3',
                  mongo_wiki_host: str = 'localhost',
                  use_ngrams: bool = False,
                  ngram_size: int = 3) -> TextGenerator:
    global __model
    if not __model:
        if not train:
            __model = TextGenerator(pg_chain=__get_chain_storage(pg_chain_host),
                                    pg_encoder=__get_encoder_storage(pg_encoder_host),
                                    model_name=model_name,
                                    state_size=3,
                                    use_ngrams=use_ngrams,
                                    ngram_size=ngram_size)
        elif train_corpus and train:
            __model = TextGenerator(pg_chain=__get_chain_storage(pg_chain_host),
                                    pg_encoder=__get_encoder_storage(pg_encoder_host),
                                    input_text=train_corpus,
                                    model_name=model_name,
                                    state_size=3,
                                    use_ngrams=use_ngrams,
                                    ngram_size=ngram_size)
        else:
            __model = get_db_model(
                model_name=model_name,
                pg_chain=__get_chain_storage(pg_chain_host),
                pg_encoder=__get_encoder_storage(pg_encoder_host),
                mongo_wiki=__get_wiki_storage(mongo_wiki_host),
                pg_habr=__get_habr_storage(pg_habs_host),
                wiki_articles_count=1000,
                habr_posts_count=1000,
                use_ngrams=use_ngrams,
                ngram_size=ngram_size,
            )
    return __model
