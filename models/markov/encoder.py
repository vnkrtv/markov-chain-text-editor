import json
from typing import Generator
from .chain import BEGIN, END


class WordsEncoder:
    counter: int
    word2int: dict
    int2word: dict

    def __init__(self, text_corpus, counter=None, word2int=None, int2word=None):
        if not text_corpus:
            self.counter = counter
            self.word2int = word2int
            self.int2word = int2word
        else:
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

    def to_dict(self):
        """
        Returns the underlying data as a Python dict.
        """
        return {
            "counter": self.counter,
            "word2int": self.word2int,
            "int2word": self.int2word
        }

    def to_json(self):
        """
        Returns the underlying data as a JSON string.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, obj):

        word2int = obj["word2int"]
        word2int[END] = word2int.pop(str(END))
        word2int[BEGIN] = word2int.pop(str(BEGIN))

        int2word = obj["int2word"]
        for key in int2word:
            int2word[int(key)] = int2word.pop(key)

        return cls(
            None,
            counter=obj["counter"],
            word2int=word2int,
            int2word=int2word
        )

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))
