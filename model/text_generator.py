import re
import logging
from typing import Iterable

import nltk
from .chain_storage import ChainStorage
from .utils import EncoderStorage, WordsEncoder, TextProcessor


class TextGenerator:
    pg_chain: ChainStorage
    pg_encoder: EncoderStorage
    encoder: WordsEncoder
    model_name: str
    state_size: int
    use_ngrams: bool
    ngram_size: int
    re_process: re.Pattern = re.compile(r'[^a-zA-Zа-яА-ЯёЁ ]')

    def __init__(self,
                 pg_chain: ChainStorage,
                 pg_encoder: EncoderStorage,
                 model_name: str,
                 state_size: int,
                 input_text: Iterable = None,
                 use_ngrams: bool = False,
                 ngram_size: int = 3):
        self.pg_chain = pg_chain
        self.pg_encoder = pg_encoder
        self.model_name = model_name
        self.state_size = state_size
        self.use_ngrams = use_ngrams
        self.ngram_size = ngram_size
        if input_text:
            self.train_model(input_text)
        else:
            self.encoder = self.pg_encoder.load_encoder(model_name)
        logging.info(f'Load model: {self}')

    def train_model(self, input_text: Iterable):
        if self.use_ngrams:
            train_corpus = list(TextProcessor.get_ngram_gen(input_text, self.ngram_size))
        else:
            train_corpus = list(TextProcessor.get_text_gen(input_text))

        self.encoder = WordsEncoder()
        encoded_train_corpus = self.encoder.fit_encode(train_corpus)

        self.pg_encoder.add_encoder(self.model_name, self.encoder)
        self.pg_chain.add_model(self.model_name, encoded_train_corpus, self.state_size)
        logging.info(f'Add new model: {self}')

    def delete_model(self):
        self.pg_chain.delete_model(self.model_name)
        self.pg_encoder.delete_encoder(self.model_name)
        logging.info(f'Delete model: {self}')

    def ngrams_split(self, sentence: str) -> list:
        processed_sentence = self.re_process.sub('', sentence.lower())
        ngrams_list = [''.join(item) for item in nltk.ngrams(processed_sentence, self.ngram_size)]
        return ngrams_list

    def words_split(self, sentence: str) -> list:
        words_list = []
        for word in sentence.split():
            processed_word = self.re_process.sub('', word.lower())
            if processed_word:
                words_list.append(processed_word)
        return words_list

    def res_join(self, words_list: list) -> str:
        return ' '.join(words_list)

    def make_sentence(self, init_state: list, **kwargs):
        tries = kwargs.get('tries', 10)
        max_words = kwargs.get('max_words', None)
        min_words = kwargs.get('min_words', None)

        if init_state is not None:
            init_state = self.encoder.encode_words_list(init_state)
            prefix = init_state
            for word in prefix:
                if word == self.encoder.begin_word:
                    prefix = prefix[1:]
                else:
                    break
        else:
            prefix = []

        for _ in range(tries):
            codes_list = prefix + self.pg_chain.walk(self.model_name, init_state, 100)
            words_list = self.encoder.decode_codes_list(codes_list)
            if (max_words is not None and len(words_list) > max_words) or (
                    min_words is not None and len(words_list) < min_words):
                continue
            return self.res_join(words_list)
        return None

    def make_sentence_with_start(self, input_phrase: str, **kwargs):
        if self.use_ngrams:
            items_list = self.ngrams_split(input_phrase)
        else:
            items_list = self.words_split(input_phrase)
        items_count = len(items_list)

        if items_count == self.state_size:
            init_state = items_list

        elif 0 < items_count < self.state_size:
            init_state = [self.encoder.begin_word] * (self.state_size - items_count) + items_list
        else:
            init_state = [self.encoder.begin_word] * self.state_size

        return self.make_sentence(init_state, **kwargs)

    def make_sentences_for_t9(self,
                              beginning: str,
                              first_words_count: int = 1,
                              count: int = 30,
                              phrase_len: int = 5,
                              **kwargs) -> list:
        phrases = set()
        logging.info("Model '%s' - beginning: %s", self.model_name, beginning)
        for i in range(count):
            phrase = self.make_sentence_with_start(beginning, min_words=phrase_len, **kwargs)
            print(phrase)
            if phrase:
                words_list = phrase.split()
                if 1 < len(words_list) >= phrase_len:
                    phrases.add(" ".join(words_list[first_words_count:]))
        logging.info("Model '%s' - executed: %s", self.model_name, '\n'.join(phrases))
        return list(phrases)

    def __repr__(self):
        return '<TextGenerator: model_name=%s, state_size=%s, ngrams=%s>' % (
            self.model_name,
            self.state_size,
            str(self.use_ngrams) + ', ngram_size=' + str(self.ngram_size) if self.use_ngrams else self.use_ngrams)

