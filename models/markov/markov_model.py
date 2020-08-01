import os
import markovify


class MarkovModel:

    model: markovify.NewlineText

    def __init__(self, input_text='', model=None, state_size=2):
        if model:
            self.model = model
        elif input_text:
            self.model = markovify.NewlineText(input_text, state_size=state_size)

    def compile(self):
        self.model.compile(inplace=True)
        return self

    @classmethod
    def load(cls, model_name='model1.0-habr-10000.json', models_path='models/markov/bin'):
        with open(os.path.join(models_path, model_name), 'r') as f:
            model_json = f.read()
        model = markovify.Text.from_json(model_json)
        return cls(model=model)

    def save(self, model_name):
        with open(f'models/markov/bin/{model_name}.json', 'w') as f:
            f.write(self.model.to_json())

    def generate_sample(self, beginning: str) -> str:
        return self.model.make_sentence_with_start(beginning)

    def get_words_for_t9(self, beginning: str, count=20) -> list:
        words = set()
        for i in range(count):
            phrase = self.generate_sample(beginning)
            if phrase:
                words_list = phrase.split()
                if len(words_list) > 1:
                    words.add(words_list[1])
        return list(words)

