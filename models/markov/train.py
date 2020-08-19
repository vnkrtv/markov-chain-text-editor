from models.utils import mongo, postgres
from models.markov.markov_model import MarkovModel
from models.markov.text_processor import TextProcessor


def get_markov_model(
        mongo_storage: mongo.MongoStorage,
        postgres_storage: postgres.PostgresStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3
):
    habr_posts = postgres_storage.get_posts_texts(
        count=habr_posts_count)
    wiki_articles = mongo_storage.get_articles_headings_texts(
        count=wiki_articles_count)
    input_text = TextProcessor.process_text_list(
        text_list=habr_posts + wiki_articles,
        window_size=model_state)
    model = MarkovModel(input_text, state_size=model_state)
    return model.compile()


def get_markov_model_with_gen_inputs(
        mongo_storage: mongo.MongoStorage,
        postgres_storage: postgres.PostgresStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3
):
    habr_posts_gen = postgres_storage.get_posts_texts_gen(
        count=habr_posts_count)
    wiki_articles_gen = mongo_storage.get_articles_headings_texts_gen(
        count=wiki_articles_count)
    text_gen = TextProcessor.get_text_gen(
        text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)),
        window_size=model_state)
    model = MarkovModel(text_gen, state_size=model_state)
    return model.compile()
