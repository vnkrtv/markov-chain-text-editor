from typing import Generator
from .chain import BEGIN, END


class WordsEncoder:
    counter: int
    word2int: dict
    int2word: dict

    def __init__(self, text_corpus):
        self.counter = 0
        self.word2int = {
            BEGIN: 0,
            END: -1
        }
        self.int2word = {
            0: BEGIN,
            -1: END
        }
        is_gen = isinstance(text_corpus, Generator)
        for sentence in text_corpus:
            if is_gen:
                sentence = sentence.split()
            for word in sentence:
                if word not in self.word2int:
                    self.counter += 1
                    self.word2int[word] = self.counter
                    self.int2word[self.counter] = word

    def encode_words_list(self, words_list: list) -> list:
        return [self.word2int[word] for word in words_list]

    def encode_text_corpus(self, text_corpus: list) -> list:
        """List of lists of words"""
        return [self.encode_words_list(words_list) for words_list in text_corpus]

    def encode_text_corpus_gen(self, text_corpus_gen: Generator) -> Generator:
        """List of lists of words"""
        return (self.encode_words_list(sentence.split()) for sentence in text_corpus_gen)

    def decode_codes_list(self, codes_list: list) -> list:
        return [self.int2word[code] for code in codes_list]
