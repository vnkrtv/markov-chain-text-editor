from models import (
    MarkovModel, MongoStorage, PostgresStorage, get_markov_model_with_gen_inputs)

__mongo_storage: MongoStorage = None
__postgres_storage: PostgresStorage = None
__model: MarkovModel = None


def __get_mongo_storage() -> MongoStorage:
    global __mongo_storage
    if not __mongo_storage:
        __mongo_storage = MongoStorage.connect(
            host='localhost')
    return __mongo_storage


def __get_postgres_storage() -> PostgresStorage:
    global __postgres_storage
    if not __postgres_storage:
        __postgres_storage = PostgresStorage.connect(
            host='172.17.0.2')
    return __postgres_storage


def get_model(model_name=None) -> MarkovModel:
    global __model
    if not __model:
        if model_name:
            __model = MarkovModel.load(model_name)
        else:
            __model = get_markov_model_with_gen_inputs(
                mongo_storage=__get_mongo_storage(),
                postgres_storage=__get_postgres_storage(),
                model_state=3,
                wiki_articles_count=1000,
                habr_posts_count=1000
            )
            # __model.save(model_name)
    return __model
