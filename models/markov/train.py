from models.utils import mongo, postgres
from models.markov.markov_model import MarkovModel
from models.markov.text_processor import TextProcessor


def get_wiki_articles(
        mongo_storage: mongo.MongoStorage,
        articles_count=1000,
):
    return mongo_storage.get_articles_headings_texts(articles_count)


def get_habr_posts(
        postgres_storage: postgres.PostgresStorage,
        posts_count=1000,
):
    return postgres_storage.get_posts_texts(posts_count)


def get_markov_model(
        mongo_storage: mongo.MongoStorage,
        postgres_storage: postgres.PostgresStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3
):
    habr_posts = get_habr_posts(
        postgres_storage=postgres_storage,
        posts_count=habr_posts_count)
    wiki_articles = get_wiki_articles(
        mongo_storage=mongo_storage,
        articles_count=wiki_articles_count
    )
    input_text = TextProcessor.process_text_list(
        text_list=habr_posts + wiki_articles
    )
    model = MarkovModel(input_text, state_size=model_state)
    return model.compile()
