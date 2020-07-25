import re


class TextProcessor:

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
