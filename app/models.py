from datetime import datetime, timedelta
from typing import Iterable
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login
from model import TextGenerator
from .markov import set_model, get_encoder_storage, get_chain_storage


@login.user_loader
def load_user(_id):
    return User.query.get(int(_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
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
    title = db.Column(db.String(256))
    body = db.Column(db.Text(), default='')
    created = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=3))
    last_update = db.Column(db.DateTime, default=lambda: datetime.utcnow() + timedelta(hours=3))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Document: {}>'.format(self.title)


class MarkovModel(db.Model):
    __tablename__ = 'markov_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    state_size = db.Column(db.Integer)
    use_ngrams = db.Column(db.Boolean)
    ngram_size = db.Column(db.Integer)

    @classmethod
    def train(cls,
              train_corpus: Iterable,
              model_name: str,
              state_size: int,
              use_ngrams: bool,
              ngram_size: int):
        model = TextGenerator(pg_chain=get_chain_storage(),
                              pg_encoder=get_encoder_storage(),
                              input_text=train_corpus,
                              model_name=model_name,
                              state_size=3,
                              use_ngrams=use_ngrams,
                              ngram_size=ngram_size)
        set_model(model)
        return cls(name=model_name,
                   state_size=state_size,
                   use_ngrams=use_ngrams,
                   ngram_size=ngram_size)

    def load(self):
        model = TextGenerator(pg_chain=get_chain_storage(),
                              pg_encoder=get_encoder_storage(),
                              model_name=self.name,
                              state_size=self.state_size)
        set_model(model)

    def __repr__(self):
        return '<Markov model: %s, state size=%s, ngrams=%s>' % (
            self.name,
            self.state_size,
            str(self.use_ngrams) + ', ngram_size=' + str(self.ngram_size) if self.use_ngrams else self.use_ngrams)
