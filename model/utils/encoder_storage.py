import psycopg2

from .postgres import PostgresStorage
from .encoder import WordsEncoder


class EncoderStorage(PostgresStorage):
    model_name: str
    begin_word: int = 0
    end_word: int = -1

    def add_encoder(self, model_name: str, encoder: WordsEncoder):
        self.model_name = model_name

        self.exec('CALL add_encoder(%s)', [model_name])

        cursor = self.conn.cursor()
        for code, word in encoder.int2word.items():
            sql = f'''INSERT INTO {model_name}_encoder(code, word)
                      VALUES (%s, %s)'''
            cursor.execute(sql, [code, word])
        self.conn.commit()

    def delete_encoder(self, model_name: str):
        self.exec('CALL delete_encoder(%s)', [model_name])

    def load_encoder(self, model_name: str) -> WordsEncoder:
        int2word = {}
        word2int = {}
        for row in self.exec_query(f'SELECT code, word FROM {model_name}_encoder', []):
            code, word = row[0], row[1]
            int2word[code] = word
            word2int[word] = code
        word2int[self.end_word] = int(word2int.pop(str(self.end_word)))
        word2int[self.begin_word] = int(word2int.pop(str(self.begin_word)))
        counter = len(int2word) - 2  # except begin and end words
        return WordsEncoder(counter=counter,
                            int2word=int2word,
                            word2int=word2int)
