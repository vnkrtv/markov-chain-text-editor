import random
from collections import deque
import re


def generate_random_start(model):
    # Чтобы сгенерировать любое начальное слово, раскомментируйте строку:
    # return random.choice(model.keys())

    # Чтобы сгенерировать "правильное" начальное слово, используйте код ниже:
    # Правильные начальные слова - это те, что являлись началом предложений в корпусе
    if 'END' in model:
        seed_word = 'END'
        while seed_word == 'END':
            seed_word = model['END'].return_weighted_random_word()
        return seed_word
    return random.choice(list(model.keys()))


def generate_random_sentence(length, markov_model):
    current_word = generate_random_start(markov_model)
    sentence = [current_word]
    for i in range(0, length):
        current_dictogram = markov_model[current_word]
        random_weighted_word = current_dictogram.return_weighted_random_word()
        current_word = random_weighted_word
        sentence.append(current_word)
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'

def generate_random_sentence_for_higher_model(length, markov_model):
    current_words = generate_random_start(markov_model)
    sentence = list(current_words)
    for i in range(0, length):
        if isinstance(current_words, str):
            samples_list = []
            for i in higher_order_markov_model:
                if i[0] == current_words:
                    samples_list.append(i)
            current_words = random.choice(samples_list)
        current_dictogram = markov_model[current_words]
        random_weighted_words = current_dictogram.return_weighted_random_word()
        current_words = random_weighted_words            
        sentence.append(current_words)
    sentence[0] = sentence[0].capitalize()
    return ' '.join(sentence) + '.'