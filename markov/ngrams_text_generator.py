import json
from typing import Iterable, List, Dict, Any

from config import Config
from .encoded_chain import EncodedChain
from .utils import TextProcessor


class NgrammTextGenerator:
    chain: EncodedChain
    model_name: str
    state_size: int
    ngram_size: int

    def __init__(self,
                 model_name: str,
                 chain: EncodedChain = None,
                 state_size: int = None,
                 ngram_size: int = None):
        if model_name and chain and state_size and ngram_size:
            self.model_name = model_name
            self.chain = chain
            self.state_size = state_size
            self.ngram_size = ngram_size

    @classmethod
    def load(cls, model_name: str):
        with open(Config.MODELS_ROOT / (model_name + '.json'), 'r') as f:
            obj = json.load(f)
        chain = EncodedChain.from_json(obj['chain'])
        return cls(model_name=obj['model_name'],
                   chain=chain,
                   state_size=chain.state_size,
                   ngram_size=obj['ngram_size'])

    @classmethod
    def train(cls,
              model_name: str,
              train_text: Iterable,
              state_size: int,
              ngram_size: int):
        train_corpus = list(TextProcessor.get_ngram_gen(train_text, ngram_size))
        chain = EncodedChain(train_corpus, state_size)
        model = cls(model_name=model_name,
                    chain=chain,
                    state_size=state_size,
                    ngram_size=ngram_size)
        model.dump()
        return model

    def ngrams_split(self, sentence: str) -> List[str]:
        ngrams_list = next(TextProcessor.get_ngram_gen([sentence], self.ngram_size))
        return ngrams_list

    def ngrams_join(self, ngrams_list: List[str]) -> str:
        return ngrams_list[0][:-1] + ''.join([ngram[-1] for ngram in ngrams_list])

    def make_sentence(self, init_state: List[str], **kwargs) -> List[str]:
        tries = kwargs.get('tries', 10)
        max_words = kwargs.get('max_words', None)
        min_words = kwargs.get('min_words', None)

        for _ in range(tries):
            chars_list = self.chain.walk(tuple(init_state))
            if (max_words is not None and len(chars_list) > max_words) or (
                    min_words is not None and len(chars_list) < min_words):
                continue
            return chars_list
        return []

    def make_sentence_with_start(self, input_phrase: str, **kwargs) -> str:
        items_list = self.ngrams_split(input_phrase)
        items_count = len(items_list)

        if items_count == self.state_size:
            init_state = items_list

        elif self.state_size < items_count:
            init_state = items_list[-self.state_size:]
        else:
            return ''

        chars_list = self.make_sentence(init_state, **kwargs)
        return self.ngrams_join(items_list) + ''.join(chars_list)

    def make_sentences_for_t9(self,
                              beginning: str,
                              first_words_count: int = 1,
                              count: int = 30,
                              phrase_len: int = 5,
                              **kwargs) -> List[str]:
        phrases = set()
        print("Model '%s' - beginning: %s" % (self.model_name, beginning))
        for i in range(count):
            phrase = self.make_sentence_with_start(beginning, min_words=phrase_len, **kwargs)
            print(phrase)
            if phrase:
                words_list = phrase.split()
                if 1 < len(words_list) >= phrase_len:
                    phrases.add(" ".join(words_list[first_words_count:]))
        return list(phrases)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'state_size': self.state_size,
            'ngram_size': self.ngram_size,
            'chain': self.chain.model
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def dump(self):
        with open(Config.MODELS_ROOT / (self.model_name + '.json'), 'w') as f:
            json.dump(self.to_json(), f, indent=4)

    def __repr__(self) -> str:
        return '<TextGenerator: state_size=%s, ngrams_size=%s>' % (
            self.state_size, self.ngram_size)
