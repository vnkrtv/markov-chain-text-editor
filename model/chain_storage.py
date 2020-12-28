from typing import Iterable

from .utils import PostgresStorage


class ChainStorage(PostgresStorage):
    begin_word: int = 0
    end_word: int = -1

    def add_model(self, model_name: str, train_corpus: Iterable, state_size: int):
        cursor = self.conn.cursor()

        hash_index = True
        for encoded_sentence in train_corpus:
            if encoded_sentence:
                cursor.execute('CALL update_chain(%s, %s, %s, %s)',
                               [encoded_sentence, state_size, self.begin_word, self.end_word])

        cursor.execute('CALL add_model(%s, %s, %s)', [model_name, self.end_word, hash_index])
        self.conn.commit()

    def delete_model(self, model_name: str):
        self.exec('CALL delete_model(%s)', [model_name])

    def walk(self, model_name: str, init_state: list, phrase_len: int = 10):
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT chain_walk_{model_name}(%s, %s)', [init_state, phrase_len])
        return cursor.fetchone()[0] or []
