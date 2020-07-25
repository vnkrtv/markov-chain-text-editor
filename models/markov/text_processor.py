import re


class Tokenizer:

    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')
    remove_brackets = re.compile(r' \((.*?)\)')

    @classmethod
    def tokenize(cls, text: str, remove_brackets=True, remove_endings=True) -> list:
        buf = text.split('\n')
        buf = [item for item in buf if item]
        sentences = []
        if not remove_endings:
            for sentence in cls.to_sentences.split(' '.join(buf)):
                buf_list = [item for item in sentence.split('!') if item]
                for item in buf_list:
                    if item[-1] == '.' or item[-1] == '?':
                        sentences.append(item)
                    else:
                        sentences.append(item + '!')
        else:
            sentences = [sentence[:-1] for sentence in cls.to_sentences.split(' '.join(buf)) if sentence[:-1]]
        if remove_brackets:
            return [cls.remove_brackets.sub('', sentence) for sentence in sentences]
        return sentences


class TextProcessor:

    tokenizer = Tokenizer()

    @classmethod
    def __process_text_list(cls, text_list: list, remove_brackets=True, remove_endings=True) -> list:
        processed_text_list = []
        for text in text_list:
            processed_text_list += cls.tokenizer.tokenize(
                text=text,
                remove_brackets=remove_brackets,
                remove_endings=remove_endings)

    @classmethod
    def process(cls, text_list: list, remove_brackets=True, remove_endings=True) -> str:
        processed_text_list = cls.__process_text_list(
            text_list=text_list,
            remove_brackets=remove_brackets,
            remove_endings=remove_endings)
        processed_text = ''
        for text in processed_text_list:
            processed_text += (text + '\n')
        return text
