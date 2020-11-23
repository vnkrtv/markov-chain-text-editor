from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db, login


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

    def __repr__(self):
        return '<Markov model: %s, state size=%s, ngrams=%s>' % (
            self.name,
            self.state_size,
            self.use_ngrams + ', ngram_size=' + self.ngram_size if self.use_ngrams else self.use_ngrams)
