import re
import json
import random
from typing import Generator
from .utils import WordsEncoder
from .chain import EncodedChain, BEGIN

DEFAULT_MAX_OVERLAP_RATIO = 0.7
DEFAULT_MAX_OVERLAP_TOTAL = 15
DEFAULT_TRIES = 10


class ParamError(Exception):
    pass


class EncodedText(object):
    encoder: WordsEncoder

    reject_pat = re.compile(r"(^')|('$)|\s'|'\s|[\"(\(\)\[\])]")

    def __init__(self, input_text, state_size=2, chain=None, encoder=None):
        self.state_size = state_size
        if encoder:
            self.encoder = encoder
            if chain:
                self.chain = chain
            elif isinstance(input_text, Generator):
                self.chain = EncodedChain(input_text, state_size)
        else:
            if not chain:
                self.encoder = WordsEncoder(input_text)
                encoded_corpus = self.encoder.encode_text_corpus(input_text)
            self.chain = chain or EncodedChain(encoded_corpus, state_size)

    def compile(self, inplace=False):
        if inplace:
            self.chain.compile(inplace=True)
            return self
        cchain = self.chain.compile(inplace=False)
        return EncodedText(None,
                           state_size=self.state_size,
                           chain=cchain)

    def to_dict(self):
        """
        Returns the underlying data as a Python dict.
        """
        return {
            "state_size": self.state_size,
            "chain": self.chain.to_json(),
            "encoder": self.encoder.to_json()
        }

    def to_json(self):
        """
        Returns the underlying data as a JSON string.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, obj, **kwargs):
        return cls(
            None,
            state_size=obj["state_size"],
            chain=EncodedChain.from_json(obj["chain"]),
            encoder=WordsEncoder.from_json(obj["encoder"])
        )

    @classmethod
    def from_json(cls, json_str):
        return cls.from_dict(json.loads(json_str))

    word_split_pattern = re.compile(r"\s+")

    def word_split(self, sentence):
        """
        Splits a sentence into a list of words.
        """
        return re.split(self.word_split_pattern, sentence)

    def word_join(self, words):
        """
        Re-joins a list of words into a sentence.
        """
        return " ".join(words)

    def make_sentence(self, init_state=None, **kwargs):
        tries = kwargs.get('tries', 10)
        max_words = kwargs.get('max_words', None)
        min_words = kwargs.get('min_words', None)

        try:
            if init_state is not None:
                init_state = tuple(self.encoder.encode_words_list(init_state))
                prefix = list(init_state)
                for word in prefix:
                    if word == BEGIN:
                        prefix = prefix[1:]
                    else:
                        break
            else:
                prefix = []

            for _ in range(tries):
                words_codes = prefix + self.chain.walk(init_state)
                words = self.encoder.decode_codes_list(words_codes)
                if (max_words is not None and len(words) > max_words) or (
                        min_words is not None and len(words) < min_words):
                    continue
                return self.word_join(words)
        except KeyError:
            pass
        return None

    def make_short_sentence(self, max_chars, min_chars=0, **kwargs):
        tries = kwargs.get('tries', DEFAULT_TRIES)

        for _ in range(tries):
            sentence = self.make_sentence(**kwargs)
            if sentence and max_chars >= len(sentence) >= min_chars:
                return sentence

    def make_sentence_with_start(self, beginning, strict=True, **kwargs):
        split = tuple(self.word_split(beginning))
        word_count = len(split)

        if word_count == self.state_size:
            init_states = [split]

        elif 0 < word_count < self.state_size:
            if strict:
                init_states = [(BEGIN,) * (self.state_size - word_count) + split]

            else:
                init_states = [key for key in self.chain.model.keys()
                               # check for starting with begin as well ordered lists
                               if tuple(filter(lambda x: x != BEGIN, key))[:word_count] == split]

                random.shuffle(init_states)
        else:
            err_msg = "`make_sentence_with_start` for this self requires a string containing 1 to {0} words. Yours " \
                      "has {1}: {2}".format(
                self.state_size, word_count, str(split))
            raise ParamError(err_msg)

        for init_state in init_states:
            output = self.make_sentence(init_state, min_words=kwargs.get('min_words'), **kwargs)
            if output is not None:
                return output

        return None

    @classmethod
    def from_chain(cls, chain_json, corpus=None):
        """
        Init a Text class based on an existing chain JSON string or object
        If corpus is None, overlap checking won't work.
        """
        chain = EncodedChain.from_json(chain_json)
        return cls(corpus or None, state_size=chain.state_size, chain=chain)


class EncodedNewlineText(EncodedText):
    """
    A (usable) example of subclassing markovify.Text. This one lets you markovify
    text where the sentences are separated by newlines instead of ". "
    """

    def sentence_split(self, text):
        return re.split(r"\s*\n\s*", text)
