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

    def get_words_for_t9(self, word: str, count=10) -> list:
        words = []
        for i in range(count):
            phrase = self.generate_sample(word)
            if phrase and len(phrase.split()) > 1:
                words.append(phrase.split()[1])
        return words

