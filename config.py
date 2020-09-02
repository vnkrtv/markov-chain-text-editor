import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    PG_USER = os.environ.get('PG_USER', 'postgres')
    PG_PASS = os.environ.get('PG_PASS', 'postgres')
    PG_HOST = os.environ.get('PG_HOST', 'localhost')
    PG_PORT = os.environ.get('PG_PORT', 5432)
    PG_DBNAME = os.environ.get('PG_DBNAME', 'doc_editor')
    SQLALCHEMY_DATABASE_URI = f'postgresql://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}'
