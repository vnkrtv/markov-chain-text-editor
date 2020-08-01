from models.markov.train import get_markov_model
from models.utils import mongo, postgres
from models.markov.markov_model import MarkovModel

__mongo_storage: mongo.MongoStorage = None
__postgres_storage: postgres.PostgresStorage = None
__model: MarkovModel = None


def __get_mongo_storage():
    global __mongo_storage
    if __mongo_storage:
        return __mongo_storage
    else:
        __mongo_storage = mongo.MongoStorage.connect(
            host='localhost')
        return __mongo_storage


def __get_postgres_storage():
    global __postgres_storage
    if __postgres_storage:
        return __postgres_storage
    else:
        __postgres_storage = postgres.PostgresStorage.connect(
            host='172.17.0.2')
        return __postgres_storage


def get_model():
    global __model
    if __model:
        return __model
    else:
        __model = get_markov_model(
            mongo_storage=__get_mongo_storage(),
            postgres_storage=__get_postgres_storage(),
            model_state=3,
            wiki_articles_count=1000,
            habr_posts_count=2000
        )
        return __model
