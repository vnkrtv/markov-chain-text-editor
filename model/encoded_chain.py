from typing import Iterable, Generator, Dict, List, Any
import operator
import random
import bisect
import json


END = '__END__'


def accumulate(iterable: Iterable[Any], func=operator.add) -> Generator:
    it = iter(iterable)
    total = next(it)
    yield total
    for element in it:
        total = func(total, element)
        yield total


def compile_next(next_dict: Dict[tuple, dict]) -> List[list]:
    words = list(next_dict.keys())
    cff = list(accumulate(next_dict.values()))
    return [words, cff]


class EncodedChain:
    model: Dict[tuple, list]
    state_size: int

    def __init__(self, corpus: Iterable[list], state_size: int, model=None):
        self.state_size = state_size
        self.model = model or self.build(corpus, self.state_size)

    def get_random_init_state(self) -> tuple:
        return random.choice(list(self.model.keys()))

    def build(self, corpus, state_size) -> Dict[tuple, list]:
        model = {}

        for run in corpus:
            items = run + [END]
            for i in range(len(run) + 1 - state_size):
                state = tuple(items[i:i + state_size])
                follow = items[i + state_size]
                if follow != END:
                    follow = follow[-1]
                if state not in model:
                    model[state] = {}

                if follow not in model[state]:
                    model[state][follow] = 0

                model[state][follow] += 1

        model = {state: compile_next(next_dict) for (state, next_dict) in model.items()}
        return model

    def move(self, state: tuple) -> Any:
        choices, cumdist = self.model.get(state, [None, None])
        if not choices:
            return END
        r = random.random() * cumdist[-1]
        selection = choices[bisect.bisect(cumdist, r)]
        return selection

    def gen(self, init_state: tuple = None) -> Generator:
        state = init_state
        while True:
            next_word = self.move(state)
            if next_word == END:
                break
            yield next_word
            state = state[1:] + (state[-1][1:] + next_word,)

    def walk(self, init_state: tuple = None) -> list:
        return list(self.gen(init_state))

    def to_json(self) -> str:
        return json.dumps(list(self.model.items()))

    @classmethod
    def from_dict(cls, model: Dict[str, Any]):
        state_size = len(list(model.keys())[0])
        return cls(model=model, state_size=state_size)

    @classmethod
    def from_json(cls, json_thing: Any):
        if isinstance(json_thing, str):
            obj = json.loads(json_thing)
        else:
            obj = json_thing

        if isinstance(obj, list):
            rehydrated = dict((tuple(item[0]), item[1]) for item in obj)
        elif isinstance(obj, dict):
            rehydrated = obj
        else:
            raise ValueError("Object should be dict or list")

        state_size = len(list(rehydrated.keys())[0])

        inst = cls(None, state_size, rehydrated)
        return inst
