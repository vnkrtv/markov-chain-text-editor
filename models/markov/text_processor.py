import re
from typing import Generator
from nltk import ngrams


class Tokenizer:

    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    remove_brackets = re.compile(r' \((.*?)\)')
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    @classmethod
    def tokenize(cls, text: str, remove_punctuation=True, remove_brackets=True) -> Generator:
        buf = text.split('\n')
        buf = (item for item in buf if item)
        sentences = (sentence[:-1].lower()
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
    def __get_sentences_list(cls, text_list: list, remove_punctuation=True, remove_brackets=True) -> list:
        sentences_list = []
        for text in text_list:
            sentences_list += list(cls.tokenizer.tokenize(
                text=text,
                remove_punctuation=remove_punctuation,
                remove_brackets=remove_brackets))
        return sentences_list

    @classmethod
    def __get_sentences_gens(cls, text_gen: Generator, remove_punctuation=True, remove_brackets=True) -> Generator:
        for text in text_gen:
            yield cls.tokenizer.tokenize(
                text=text,
                remove_punctuation=remove_punctuation,
                remove_brackets=remove_brackets)

    @classmethod
    def process_text_list(cls, text_list: list, window_size=1) -> str:
        text = ''
        sentences_list = cls.__get_sentences_list(text_list)
        for sentence_num in range(len(sentences_list)):
            sentence = sentences_list[sentence_num]
            for i in range(window_size):
                text += (' '.join(sentence.split()[i:]) + '\n')
        return text[:-1]

    @classmethod
    def get_text_gen(cls, text_gen: Generator, window_size=1) -> Generator:
        for sentences_gen in cls.__get_sentences_gens(text_gen):
            for sentence in sentences_gen:
                for ngram in (' '.join(ngram) for ngram in ngrams(sentence.split(), window_size)):
                    yield ngram
