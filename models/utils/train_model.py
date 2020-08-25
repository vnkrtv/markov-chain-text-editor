from models.markov import MarkovModel, WordsEncoder
from .text_processor import TextProcessor
from .mongo import MongoStorage
from .postgres import PostgresStorage


def get_text_gen(
        mongo_storage: MongoStorage,
        postgres_storage: PostgresStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3
):
    habr_posts_gen = postgres_storage.get_posts_texts_gen(
        count=habr_posts_count)
    wiki_articles_gen = mongo_storage.get_articles_headings_texts_gen(
        count=wiki_articles_count)
    return TextProcessor.get_text_gen(
        text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)),
        window_size=model_state)


def get_markov_model(
        mongo_storage: MongoStorage,
        postgres_storage: PostgresStorage,
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
        mongo_storage: MongoStorage,
        postgres_storage: PostgresStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3
):
    kwargs = dict(
        mongo_storage=mongo_storage,
        postgres_storage=postgres_storage,
        wiki_articles_count=wiki_articles_count,
        habr_posts_count=habr_posts_count,
        model_state=model_state)
    print('Get posts and articles')
    encoder = WordsEncoder(
        text_corpus=get_text_gen(**kwargs))
    train_corpus = encoder.encode_text_corpus_gen(
        text_corpus_gen=get_text_gen(**kwargs))
    print('Get text_gen')
    model = MarkovModel(
        train_input=train_corpus,
        state_size=model_state,
        encoder=encoder)
    print('Complete training model')
    return model.compile()
