from typing import Generator
import pymongo


class MongoStorage:
    """Class for working with MongoDB"""

    db: pymongo.database.Database
    col: pymongo.collection.Collection

    def __init__(self, db: pymongo.database.Database, col: pymongo.collection.Collection):
        self.db = db
        self.col = col

    @classmethod
    def connect(cls, host: str, port=27017, db_name='wiki', col_name='articles'):
        db = pymongo.MongoClient(host, port, unicode_decode_error_handler='ignore')[db_name]
        return cls(
            db=db,
            col=db[col_name])

    def get_articles(self, count=0) -> list:
        return list(self.col.find({}).limit(count))

    def get_articles_gen(self, count=0) -> Generator:
        return self.col.find({}).limit(count)

    def get_article(self, title) -> dict:
        doc = self.col.find_one({'title': title})
        return doc if doc else {}

    def get_articles_headings_texts(self, count=0) -> list:
        articles = self.get_articles(count)
        return [article['text']['Заголовок']['text'] for article in articles]

    def get_articles_headings_texts_gen(self, count=0) -> list:
        for article in self.get_articles_gen(count):
            yield article['text']['Заголовок']['text']
