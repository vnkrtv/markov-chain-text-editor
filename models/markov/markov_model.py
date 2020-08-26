import os
from typing import Generator
from .text import EncodedText, EncodedNewlineText


class MarkovModel:

    model: EncodedText

    def __init__(self, train_input, model=None, encoder=None, state_size=2):
        if model:
            self.model = model
        elif isinstance(train_input, str):
            self.model = EncodedNewlineText(train_input, state_size=state_size)
        elif isinstance(train_input, Generator) and encoder:
            self.model = EncodedText(train_input, state_size=state_size, encoder=encoder)

    def compile(self):
        self.model.compile(inplace=True)
        return self

    @classmethod
    def load(cls, model_name, models_path='models/markov/bin'):
        with open(os.path.join(models_path, model_name), 'r') as f:
            model_json = f.read()
        model = EncodedText.from_json(model_json)
        return cls(None, model=model)

    def save(self, model_name, models_path='models/markov/bin'):
        with open(os.path.join(models_path, model_name), 'w') as f:
            f.write(self.model.to_json())

    def generate_sample(self, beginning: str, **kwargs) -> str:
        return self.model.make_sentence_with_start(beginning, **kwargs)

    def get_phrases_for_t9(self, beginning: str, first_words_count=1, count=20, **kwargs) -> list:
        phrases = set()
        for i in range(count):
            phrase = self.generate_sample(beginning, **kwargs)
            if phrase:
                words_list = phrase.split()
                if len(words_list) > 1:
                    phrases.add(" ".join(words_list[first_words_count:]))
        return list(phrases)

