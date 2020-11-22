from .postgres import PostgresStorage
from .encoder import WordsEncoder


class EncoderStorage(PostgresStorage):
    model_name: str
    begin_word: int = 0
    end_word: int = -1

    def add_encoder(self, model_name: str, encoder: WordsEncoder):
        self.model_name = model_name

        cursor = self.conn.cursor()
        cursor.execute('CALL add_encoder(%s)', [model_name])
        self.conn.commit()

        for code, word in encoder.int2word.items():
            sql = f'''INSERT INTO {model_name}_encoder(code, word)
                      VALUES (%s, %s)'''
            cursor.execute(sql, [code, word])
        self.conn.commit()
        self.__create_indexes(model_name)

    def delete_encoder(self, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('CALL delete_encoder(%s)', [model_name])
        self.conn.commit()

    def load_encoder(self, model_name: str) -> WordsEncoder:
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT code, word FROM {model_name}_encoder')
        int2word = {}
        word2int = {}
        for row in cursor.fetchall():
            code, word = row[0], row[1]
            int2word[code] = word
            word2int[word] = code
        word2int[self.end_word] = int(word2int.pop(str(self.end_word)))
        word2int[self.begin_word] = int(word2int.pop(str(self.begin_word)))
        counter = len(int2word) - 2  # except begin and end words
        return WordsEncoder(counter=counter,
                            int2word=int2word,
                            word2int=word2int)

    def __create_indexes(self, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('CALL create_encoder_indexes(%s)', [model_name]);
        self.conn.commit()

    def __drop_indexes(self, model_name: str):
        cursor = self.conn.cursor()
        cursor.execute('CALL drop_encoder_indexes(%s)', [model_name]);
        self.conn.commit()
