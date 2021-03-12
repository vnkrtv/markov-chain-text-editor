import json
from typing import Generator, Iterable


class WordsEncoder:
    counter: int
    word2int: dict
    int2word: dict
    begin_word: int = 0
    end_word: int = -1

    def __init__(self, counter: int = None, word2int: dict = None, int2word: dict = None):
        self.counter = counter
        self.word2int = word2int
        self.int2word = int2word

    def fit(self, text_corpus):
        self.counter = 0
        self.word2int = {
            self.begin_word: self.begin_word,
            self.end_word: self.end_word
        }
        self.int2word = {
            self.begin_word: self.begin_word,
            self.end_word: self.end_word
        }
        for sentence in text_corpus:
            for word in sentence:
                if word not in self.word2int:
                    self.counter += 1
                    self.word2int[word] = self.counter
                    self.int2word[self.counter] = word

    def fit_encode(self, text_corpus: Iterable) -> Generator:
        corpus = list(text_corpus) if isinstance(text_corpus, Generator) else text_corpus
        self.fit(corpus)
        return self.encode_text_corpus_gen(corpus)

    def encode_words_list(self, words_list: list) -> list:
        return [self.word2int[word] for word in words_list]

    def encode_text_corpus(self, text_corpus: list) -> list:
        """List of lists of words"""
        return [self.encode_words_list(words_list) for words_list in text_corpus]

    def encode_text_corpus_gen(self, text_corpus_gen: Iterable) -> Generator:
        """List of lists of words"""
        return (self.encode_words_list(sentence) for sentence in text_corpus_gen)

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

        int2word = obj["int2word"]
        for key in int2word:
            int2word[int(key)] = int2word.pop(key)

        int2word[cls.end_word] = cls.end_word
        int2word[cls.begin_word] = cls.begin_word

        word2int = obj["word2int"]
        word2int[cls.end_word] = int(word2int.pop(str(cls.end_word)))
        word2int[cls.begin_word] = int(word2int.pop(str(cls.begin_word)))

        return cls(
            counter=obj["counter"],
            word2int=word2int,
            int2word=int2word
        )

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))

    def __repr__(self):
        return '<WordsEncoder: words_count=%s, begin_word=%s, end_word=%s>' % (
            str(self.counter), str(self.begin_word), str(self.end_word))
