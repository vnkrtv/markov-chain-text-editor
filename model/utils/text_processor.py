from typing import Generator
import re
import nltk


class Tokenizer:
    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    remove_brackets = re.compile(r' \((.*?)\)')
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    @classmethod
    def tokenize(cls, text: str, remove_punctuation=True, remove_brackets=True) -> Generator:
        buf = text.split('\n')
        buf = (item for item in buf if item)
        sentences = (sentence[:-1].lower().strip()
                     for sentence in cls.to_sentences.split(' '.join(buf))
                     if sentence[:-1])
        if remove_brackets:
            sentences = (cls.remove_brackets.sub('', sentence) for sentence in sentences)
        if remove_punctuation:
            return (cls.remove_punctuation.sub('', sentence) for sentence in sentences)
        return sentences


class TextProcessor:
    tokenizer = Tokenizer()

    @classmethod
    def __get_sentences_gens(cls, text_gen: Generator, remove_punctuation=True, remove_brackets=True) -> Generator:
        for text in text_gen:
            yield cls.tokenizer.tokenize(
                text=text,
                remove_punctuation=remove_punctuation,
                remove_brackets=remove_brackets)

    @classmethod
    def get_text_gen(cls, text_gens_gen) -> Generator:
        for text_gen in text_gens_gen:
            for sentences_gen in cls.__get_sentences_gens(text_gen):
                for sentence in sentences_gen:
                    yield sentence

    @classmethod
    def get_ngram_gen(cls, text_gens_gen: Generator, state_size=1) -> Generator:
        for text_gen in text_gens_gen:
            for sentences_gen in cls.__get_sentences_gens(text_gen):
                for sentence in sentences_gen:
                    for ngram in (' '.join(ngram) for ngram in nltk.ngrams(sentence.split(), state_size)):
                        yield ngram
