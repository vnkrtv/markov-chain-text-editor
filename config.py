import os
import pathlib


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    ELASTIC_HOST = os.environ.get('ELASTIC_HOST', 'localhost')
    ELASTIC_SHARDS_NUMBER = os.environ.get('ELASTIC_SHARDS_NUMBER', 1)
    ELASTIC_REPLICAS_NUMBER = os.environ.get('ELASTIC_REPLICAS_NUMBER', 2)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + str(pathlib.Path(__file__).parent / 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # PG_USER = os.environ.get('PG_USER', 'postgres')
    # PG_PASS = os.environ.get('PG_PASS', 'password')
    # PG_HOST = os.environ.get('PG_HOST', '172.17.0.2')
    # PG_PORT = os.environ.get('PG_PORT', 5432)
    # PG_DBNAME = os.environ.get('PG_DBNAME', 't9app')
    # SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'
    # MODELS_ROOT = pathlib.Path(__file__).parent / 'engine' / 'markov' / 'models'
