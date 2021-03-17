from typing import Generator, Iterable
import re

import nltk
import razdel


class Tokenizer:
    remove_punctuation = re.compile(r'[^а-яА-ЯёЁ ]')

    @classmethod
    def tokenize(cls, text: str) -> Generator:
        return (cls.remove_punctuation.sub('', sentence.text.lower().strip())
                for sentence in razdel.sentenize(text))


class TextProcessor:
    tokenizer = Tokenizer()

    @classmethod
    def get_sentences_gens(cls, texts: Iterable) -> Generator:
        for text in texts:
            for sentence in cls.tokenizer.tokenize(text):
                yield sentence

    @classmethod
    def get_words_gen(cls, text_gen: Iterable) -> Generator:
        for sentence in cls.get_sentences_gens(text_gen):
            yield [_.text for _ in razdel.tokenize(sentence)]

    @classmethod
    def get_ngram_gen(cls, text_gen: Iterable, ngram_size: int = 3) -> Generator:
        for sentence in cls.get_sentences_gens(text_gen):
            yield [''.join(item) for item in nltk.ngrams(sentence, ngram_size)]
