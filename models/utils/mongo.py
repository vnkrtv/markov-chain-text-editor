import pymongo


class MongoStorage:
    """Class for working with MongoDB"""

    db: pymongo.database.Database

    def __init__(self, db: pymongo.database.Database):
        self.db = db

    @staticmethod
    def connect(host: str, port=27017, db_name='markov_model'):
        db = pymongo.MongoClient(host, port)[db_name]
        return MongoStorage(db)

    def add_condition(self, condition: tuple, iterable) -> None:
        col = self.db['model']
        col.insert_one()

    def update_condition(self, condition: tuple, iterable) -> None:
        col = self.db['model']