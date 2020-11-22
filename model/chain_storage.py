from typing import Iterable

from .utils import PostgresStorage
from .chain import compile_next


class ChainStorage(PostgresStorage):
    begin_word: int = 0
    end_word: int = -1

    def add_model(self, model_name: str, train_corpus: Iterable, state_size: int):
        model_dict = self.__build_model(train_corpus, state_size)

        cursor = self.conn.cursor()
        cursor.execute('CALL add_model(%s, %s)', [model_name, self.end_word])
        self.conn.commit()

        for state_tuple in model_dict:
            buf = model_dict[state_tuple]
            choices_list, cumdist_list = buf[0], buf[1]
            self.__add_state(cursor, model_name, state_tuple, choices_list, cumdist_list)
        self.conn.commit()
        self.__create_index(model_name)

        del model_dict

    def delete_model(self, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('CALL delete_model(%s)', [model_name])
        self.conn.commit()

    def walk(self, model_name: str, init_state: list, phrase_len: int = 10):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT chain_walk_{model_name}(%s, %s)', [init_state, phrase_len])
        return cursor.fetchone()[0] or []

    def __build_model(self, train_corpus, state_size: int) -> dict:
        model = {}

        for run in train_corpus:
            items = ([self.begin_word] * state_size) + run + [self.end_word]
            for i in range(len(run) + 1):
                state = tuple(items[i:i + state_size])
                follow = items[i + state_size]
                if state not in model:
                    model[state] = {}

                if follow not in model[state]:
                    model[state][follow] = 0

                model[state][follow] += 1

        model = {state: compile_next(next_dict) for (state, next_dict) in model.items()}
        return model

    def __add_state(self,
                    cursor,
                    model_name: str,
                    state: tuple,
                    choices: list,
                    cumdist: list):
        sql = f'''INSERT INTO {model_name}(state, choices, cumdist)
                  VALUES (%s, %s, %s)
                  ON CONFLICT DO NOTHING'''
        cursor.execute(sql, [list(state), choices, cumdist])

    def __create_index(self, model_name: str, hash_index: bool = True):
        cursor = self.conn.cursor()
        cursor.execute('CALL create_model_table_index(%s, %s)', [model_name, hash_index]);
        self.conn.commit()

    def __drop_index(self, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('CALL drop_model_table_index(%s)', [model_name]);
        self.conn.commit()
