import os
import markovify


class MarkovModel:

    model: markovify.NewlineText

    def __init__(self, model: markovify.NewlineText):
        self.model = model
        # self.model.compile(inplace=True)

    @classmethod
    def load(cls, model_name='model1.0-habr-10000.json', models_path='models/markov/bin'):
        with open(os.path.join(models_path, model_name), 'r') as f:
            model_json = f.read()
        model = markovify.Text.from_json(model_json)
        return cls(model=model)

    def generate_sample(self, beginning: str) -> str:
        return self.model.make_sentence_with_start(beginning)

