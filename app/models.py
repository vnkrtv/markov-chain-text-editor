from datetime import datetime, timedelta
from typing import Iterable, List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login, utils
from config import Config


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Document(db.Model):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), index=True)
    body = db.Column(db.Text(), default='')
    created = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=3))
    last_update = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=3))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return '<Document: {}>'.format(self.title)


class ModelIndex(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)

    @classmethod
    def add(cls, train_sentences: Iterable[str], model_name: str):
        es = utils.get_elastic_engine()
        es.add_index(name=model_name,
                     number_of_shards=Config.ELASTIC_SHARDS_NUMBER,
                     number_of_replicas=Config.ELASTIC_REPLICAS_NUMBER)
        for sentence in train_sentences:
            es.add_doc(index_name=model_name, text=sentence)
        return cls(name=model_name)

    def generate_samples(self, beginning: str, samples_num: int) -> List[str]:
        es = utils.get_elastic_engine()
        return es.get(index_name=self.name, phrase=beginning, count=samples_num)

    def __repr__(self) -> str:
        return '<ModelIndex: %s>' % self.name
