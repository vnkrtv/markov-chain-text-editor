import re


class Tokenizer:

    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    remove_brackets = re.compile(r' \((.*?)\)')
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    @classmethod
    def tokenize(cls, text: str, remove_punctuation=True, remove_brackets=True, remove_endings=True) -> list:
        buf = text.split('\n')
        buf = [item for item in buf if item]
        sentences = []
        if not remove_endings:
            for sentence in cls.to_sentences.split(' '.join(buf)):
                buf_list = [item for item in sentence.split('!') if item]
                for item in buf_list:
                    if item[-1] == '.' or item[-1] == '?':
                        sentences.append(item.lower())
                    else:
                        sentences.append(item.lower() + '!')
        else:
            sentences = [sentence[:-1].lower() for sentence in cls.to_sentences.split(' '.join(buf)) if sentence[:-1]]
        if remove_brackets:
            sentences = [cls.remove_brackets.sub('', sentence) for sentence in sentences]
        if remove_punctuation:
            return [cls.remove_punctuation.sub('', sentence) for sentence in sentences]
        return sentences


class TextProcessor:

    tokenizer = Tokenizer()

    @classmethod
    def __get_sentences_list(cls, text_list: list, remove_brackets=True, remove_endings=True) -> list:
        sentences_list = []
        for text in text_list:
            sentences_list += cls.tokenizer.tokenize(
                text=text,
                remove_brackets=remove_brackets,
                remove_endings=remove_endings)
        return sentences_list

    @classmethod
    def process_text_list(cls, text_list: list, window_size=1, remove_brackets=True, remove_endings=True) -> str:
        text = ''
        sentences_list = cls.__get_sentences_list(
            text_list=text_list,
            remove_brackets=remove_brackets,
            remove_endings=remove_endings)
        for sentence_num in range(len(sentences_list)):
            sentence = sentences_list[sentence_num]
            for i in range(window_size):
                text += (' '.join(sentence.split()[i:]) + '\n')
        return text[:-1]
