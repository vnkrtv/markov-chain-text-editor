from .chain_storage import ChainStorage
from .text_generator import TextGenerator
from .utils import (
    TextProcessor, WikiStorage, HabrStorage, EncoderStorage)


def get_model(
        model_name: str,
        pg_chain: ChainStorage,
        pg_encoder: EncoderStorage,
        # mongo_wiki: WikiStorage,
        pg_habr: HabrStorage,
        # wiki_articles_count: int = 1000,
        habr_posts_count: int = 1000,
        use_ngrams: bool = False,
        ngram_size: int = 3,
        **kwargs
):
    habr_posts_gen = pg_habr.get_posts_texts(
        count=habr_posts_count, habs_list=kwargs.get('habs_list'), tags_list=kwargs.get('tags_list'))
    # wiki_articles_gen = mongo_wiki.get_articles_headings_texts(count=wiki_articles_count)
    if use_ngrams:
        input_gen = TextProcessor.get_ngram_gen(
            text_gen=habr_posts_gen,
            ngram_size=ngram_size)
    else:
        input_gen = TextProcessor.get_text_gen(
            text_gen=habr_posts_gen)
    model = TextGenerator(model_name=model_name,
                          pg_chain=pg_chain,
                          pg_encoder=pg_encoder,
                          state_size=3,
                          input_text=input_gen,
                          use_ngrams=use_ngrams,
                          ngram_size=ngram_size)
    return model
