import re
import random
from models.markov.histograms import Dictogram
from models.markov.text_processor import TextProcessor


class MarkovModel:

    model: dict
    order: int

    def __init__(self, order=1):
        self.model = dict()
        self.order = order

    def train(self, texts_list: list):
        contain_rus = re.compile(r'[а-яА-Я]')
        for text in texts_list:
            if contain_rus.search(text):
                for sentence in TextProcessor.tokenize(text):
                    words_list = sentence.split()
                    words_list[-1] = words_list[-1][:-1]
                    if len(words_list) > 1:
                        self.update(words_list)

    def update(self, words_list: list):
        for i in range(0, len(self.model) - self.order):
            # Создаем окно
            window = tuple(self.model[i: i + self.order])
            # Добавляем в словарь
            if window in self.model:
                # Присоединяем к уже существующему распределению
                self.model[window].update([words_list[i + self.order]])
            else:
                self.model[window] = Dictogram([words_list[i + self.order]])

    def generate_random_start(self):
        key = random.choice(list(self.model.keys()))
        # Чтобы сгенерировать любое начальное слово, раскомментируйте строку:
        # return random.choice(gpt-2.keys())

        # Чтобы сгенерировать "правильное" начальное слово, используйте код ниже:
        # Правильные начальные слова - это те, что являлись началом предложений в корпусе
        if 'END' in model:
            seed_word = 'END'
            while seed_word == 'END':
                seed_word = model['END'].return_weighted_random_word()
            return seed_word
        return random.choice(list(model.keys()))
