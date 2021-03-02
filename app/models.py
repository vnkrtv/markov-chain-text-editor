from datetime import datetime, timedelta
from typing import Iterable, List
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login
from markov import NgrammTextGenerator
from .utils import set_model, get_model


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


class MarkovModel(db.Model):
    __tablename__ = 'models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    state_size = db.Column(db.Integer)
    ngram_size = db.Column(db.Integer)

    @classmethod
    def train(cls,
              train_corpus: Iterable,
              model_name: str,
              state_size: int,
              ngram_size: int):
        model = NgrammTextGenerator.train(model_name=model_name,
                                          train_text=train_corpus,
                                          state_size=state_size,
                                          ngram_size=ngram_size)
        set_model(model)
        return cls(name=model_name,
                   state_size=state_size,
                   ngram_size=ngram_size)

    def load(self):
        model = NgrammTextGenerator.load(model_name=self.name)
        set_model(model)

    def generate_samples(self, beginning: str, samples_num: int) -> List[str]:
        tries_count = samples_num * 2
        counter = 0

        model = get_model()
        phrases = set()
        for i in range(samples_num):
            try:
                phrase = model.make_sentence_with_start(beginning)
                print(phrase)
                if phrase:
                    words_list = phrase.split()
                    if 1 < len(words_list):
                        phrases.add(" ".join(words_list))
                counter += 1
                if counter > tries_count:
                    break
            except Exception as e:
                print(e)
        return list(phrases)

    def __repr__(self) -> str:
        return '<Markov model: %s, state_size=%s, ngram_size=%s>' % (
            self.name,
            self.state_size,
            self.ngram_size)
