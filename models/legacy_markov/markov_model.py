import re
import random
import pickle
from models.markov.histograms import Dictogram
from models.utils.text_processor import TextProcessor


class MarkovModel:

    model: dict
    order: int
    start_words: list
    start_phrases: list

    def __init__(self, model=None, order=1, start_words=None, start_phrases=None):
        if model is None:
            model = {}
        if start_words is None:
            start_words = []
        if start_phrases is None:
            start_phrases = []
        self.model = model
        self.order = order
        self.start_words = start_words
        self.start_phrases = start_phrases

    def train(self, texts_list: list):
        contain_rus = re.compile(r'[а-яА-Я]')
        texts_list_len = len(texts_list)
        i = 0
        for text in texts_list:
            if contain_rus.search(text):
                text_words_list = []
                for sentence in TextProcessor.tokenize(text):
                    words_list = sentence.split()
                    if len(words_list) >= self.order:
                        self.start_phrases.append(tuple(words_list[:self.order]))
                        self.start_words.append(words_list[0])
                    words_list[-1] = words_list[-1][:-1]
                    text_words_list += words_list
                self.__update(text_words_list)
            i += 1
            print('(%d/%d) model length - %d' % (i, texts_list_len, len(self.model)))
            if i > 10000:
                break

    def generate_by_word(self, length, start_word=None):
        if not start_word:
            start_word = self.__generate_start_word()
        sentence = [start_word]

        samples_list = []
        for phrase in self.model:
            if phrase[0] == start_word:
                samples_list.append(phrase)
        current_words = random.choice(samples_list)

        for _ in range(1, length):
            current_dictogram = self.model[current_words]
            random_weighted_words = current_dictogram.return_weighted_random_word()
            current_words = random_weighted_words
            sentence.append(current_words)

        sentence[0] = sentence[0].capitalize()
        return ' '.join(sentence) + '.'

    def generate_by_phrase(self, length, start_phrase=None):
        if not start_phrase:
            start_phrase = self.__generate_start_phrase()
        sentence = start_phrase.split()

        samples_list = []
        for phrase in self.model:
            if [word.lower() for word in phrase[:len(sentence)]] == [word.lower() for word in sentence]:
                samples_list.append(phrase)
        current_words = random.choice(samples_list)

        for _ in range(len(sentence), length):
            current_dictogram = self.model[current_words]
            print(current_dictogram)
            random_weighted_words = current_dictogram.return_weighted_random_word()
            samples_list = []
            for phrase in self.model:
                if phrase[0].lower() == random_weighted_words:
                    samples_list.append(phrase)
            try:
                current_words = random.choice(samples_list)
            except:
                break
            sentence += current_words

        return ' '.join(sentence) + '.'

    def save(self, path='models/markov/bin/'):
        with open(path + 'model.pickle', 'wb') as handle:
            pickle.dump(self.model, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path + 'order.pickle', 'wb') as handle:
            pickle.dump(self.order, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path + 'start_words.pickle', 'wb') as handle:
            pickle.dump(self.start_words, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open(path + 'start_phrases.pickle', 'wb') as handle:
            pickle.dump(self.start_phrases, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path='models/markov/bin/'):
        with open(path + 'model.pickle', 'rb') as handle:
            model = pickle.load(handle)
        with open(path + 'order.pickle', 'rb') as handle:
            order = pickle.load(handle)
        with open(path + 'start_words.pickle', 'rb') as handle:
            start_words = pickle.load(handle)
        with open(path + 'start_phrases.pickle', 'rb') as handle:
            start_phrases = pickle.load(handle)
        return MarkovModel(
            model=model,
            order=order,
            start_words=start_words,
            start_phrases=start_phrases
        )

    def __update(self, words_list: list):
        for i in range(0, len(words_list) - self.order):
            # Создаем окно
            window = tuple(words_list[i: i + self.order])
            # Добавляем в словарь
            if window in self.model:
                # Присоединяем к уже существующему распределению
                self.model[window].update([words_list[i + self.order]])
            else:
                self.model[window] = Dictogram([words_list[i + self.order]])

    def __generate_start_word(self):
        return random.choice(list(self.start_words))

    def __generate_start_phrase(self):
        return random.choice(list(self.start_phrases))
