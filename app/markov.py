import os

from config import BASE_DIR
from model import (
    MarkovModel, WikiStorage, HabrStorage, get_ram_model)

RAM_MODELS_LIST = os.listdir(os.path.join(BASE_DIR, 'model', 'bin'))
MODEL_NAME = RAM_MODELS_LIST[0] if RAM_MODELS_LIST else None

__mongo_storage: WikiStorage = None
__postgres_storage: HabrStorage = None
__model: MarkovModel = None


def __get_mongo_storage(mongo_host: str) -> WikiStorage:
    global __mongo_storage
    if not __mongo_storage:
        __mongo_storage = WikiStorage.connect(
            host=mongo_host)
    return __mongo_storage


def __get_postgres_storage(postgres_host: str) -> HabrStorage:
    global __postgres_storage
    if not __postgres_storage:
        __postgres_storage = HabrStorage.connect(
            host=postgres_host)
    return __postgres_storage


def get_model(model_name: str = None,
              postgres_host: str = '172.17.0.2',
              mongo_host: str = 'localhost') -> MarkovModel:
    global __model
    if not __model:
        if model_name:
            __model = MarkovModel.load(model_name)
        else:
            __model = get_ram_model(
                mongo_storage=__get_mongo_storage(mongo_host),
                postgres_storage=__get_postgres_storage(postgres_host),
                model_state=3,
                wiki_articles_count=1000,
                habr_posts_count=1000
            )
            __model.save(model_name)
    return __model
