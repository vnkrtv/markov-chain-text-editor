from typing import Generator, Iterable
import re
import nltk


class Tokenizer:
    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    remove_brackets = re.compile(r' \((.*?)\)')
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-ЯёЁ ]')

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
    def get_sentences_gens(cls, texts: Iterable, remove_punctuation=True, remove_brackets=True) -> Generator:
        for text in texts:
            yield cls.tokenizer.tokenize(
                text=text,
                remove_punctuation=remove_punctuation,
                remove_brackets=remove_brackets)

    @classmethod
    def get_text_gen(cls, text_gen: Iterable) -> Generator:
        for sentences_gen in cls.get_sentences_gens(text_gen):
            for sentence in sentences_gen:
                yield sentence.split()

    @classmethod
    def get_ngram_gen(cls, text_gen: Iterable, ngram_size: int = 3) -> Generator:
        for sentences_gen in cls.get_sentences_gens(text_gen):
            for sentence in sentences_gen:
                yield [''.join(item) for item in nltk.ngrams(sentence, ngram_size)]
