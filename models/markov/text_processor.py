import re


class TextProcessor:

    to_sentences = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s')

    @classmethod
    def tokenize(cls, text: str) -> list:
        buf = text.split('\n')
        buf = [item for item in buf if item]
        sentences = []
        for sentence in cls.to_sentences.split(' '.join(buf)):
            buf_list = [item for item in sentence.split('!') if item]
            for item in buf_list:
                if item[-1] == '.' or item[-1] == '?':
                    sentences.append(item)
                else:
                    sentences.append(item + '!')
        return sentences
