from .ram_markov_model import MarkovModel
from .utils import (
    WordsEncoder, WikiStorage, HabrStorage, TextProcessor)


def get_text_gen(
        mongo_storage: WikiStorage,
        postgres_storage: HabrStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        **kwargs
):
    habr_posts_gen = postgres_storage.get_posts_texts(
        count=habr_posts_count, habs_list=kwargs.get('habs_list'), tags_list=kwargs.get('tags_list'))
    wiki_articles_gen = mongo_storage.get_articles_headings_texts(
        count=wiki_articles_count)
    return TextProcessor.get_text_gen(
        text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)))


def get_ram_model(
        mongo_storage: WikiStorage,
        postgres_storage: HabrStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3,
        **kwargs
):
    gen_kwargs = dict(
        mongo_storage=mongo_storage,
        postgres_storage=postgres_storage,
        wiki_articles_count=wiki_articles_count,
        habr_posts_count=habr_posts_count,
        **kwargs)
    print('Get posts and articles')
    encoder = WordsEncoder()
    train_corpus = encoder.fit_encode(
        text_corpus=get_text_gen(**gen_kwargs))
    print('Get text_gen')
    model = MarkovModel(
        train_input=train_corpus,
        state_size=model_state,
        encoder=encoder)
    print('Complete training model')
    return model.compile()

def get_db_model(

)
