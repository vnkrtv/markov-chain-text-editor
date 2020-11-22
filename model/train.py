from .ram_markov_model import MarkovModel
from .chain_storage import ChainStorage
from .text_generator import TextGenerator
from .utils import (
    WordsEncoder, TextProcessor, WikiStorage, HabrStorage, EncoderStorage)


def get_ram_model(
        mongo_storage: WikiStorage,
        postgres_storage: HabrStorage,
        wiki_articles_count=1000,
        habr_posts_count=1000,
        model_state=3,
        **kwargs
):
    habr_posts_gen = postgres_storage.get_posts_texts(
        count=habr_posts_count, habs_list=kwargs.get('habs_list'), tags_list=kwargs.get('tags_list'))
    wiki_articles_gen = mongo_storage.get_articles_headings_texts(
        count=wiki_articles_count)
    print('Get posts and articles')
    text_corpus = TextProcessor.get_text_gen(
        text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)))

    encoder = WordsEncoder()
    train_corpus = encoder.fit_encode(
        text_corpus=text_corpus)
    print('Get text_gen')

    model = MarkovModel(
        train_input=train_corpus,
        state_size=model_state,
        encoder=encoder)
    print('Complete training model')
    return model.compile()


def get_db_model(
        model_name: str,
        pg_chain: ChainStorage,
        pg_encoder: EncoderStorage,
        mongo_wiki: WikiStorage,
        pg_habr: HabrStorage,
        wiki_articles_count: int = 1000,
        habr_posts_count: int = 1000,
        use_ngrams: bool = False,
        ngram_size: int = 3,
        **kwargs
):
    habr_posts_gen = pg_habr.get_posts_texts(
        count=habr_posts_count, habs_list=kwargs.get('habs_list'), tags_list=kwargs.get('tags_list'))
    wiki_articles_gen = mongo_wiki.get_articles_headings_texts(count=wiki_articles_count)
    if use_ngrams:
        input_gen = TextProcessor.get_ngram_gen(
            text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)),
            ngram_size=ngram_size)
    else:
        input_gen = TextProcessor.get_text_gen(
            text_gens_gen=(text_gen for text_gen in (habr_posts_gen, wiki_articles_gen)))
    model = TextGenerator(model_name=model_name,
                          pg_chain=pg_chain,
                          pg_encoder=pg_encoder,
                          state_size=3,
                          input_text=input_gen,
                          use_ngrams=use_ngrams,
                          ngram_size=ngram_size)
    return model
