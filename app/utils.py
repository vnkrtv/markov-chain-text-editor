import os
import re
import pathlib
from typing import Generator, Iterable, Optional, List, Tuple, Dict, Any

import textract
import pdftotext
from textract.exceptions import ExtensionNotSupported
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import app
from config import Config
from engine.markov import PostgresStorage
from engine.elastic import ElasticEngine

__es: ElasticEngine = ElasticEngine.connect(
    host=Config.ELASTIC_HOST,
    port=Config.ELASTIC_PORT,
    user=Config.ELASTIC_USER,
    password=Config.ELASTIC_PASS)


def get_elastic_engine() -> ElasticEngine:
    global __es
    return __es


def parse_query(query: str) -> Tuple[str, List[str]]:
    params = list(re.findall(r"'(.*?)'", query))
    query = re.sub(r"'(.*?)'", '%s', query)
    return query, params


def get_postgres_storage(request_dict: Dict[str, Any]) -> PostgresStorage:
    pg_host = request_dict.get('pg_host')
    pg_port = request_dict.get('pg_port')
    pg_dbname = request_dict.get('pg_dbname')
    pg_user = request_dict.get('pg_user')
    pg_password = request_dict.get('pg_password')
    return PostgresStorage.connect(
        host=pg_host, port=pg_port, dbname=pg_dbname, user=pg_user, password=pg_password)


def get_text_corpus_from_postgres(request_dict: Dict[str, Any]) -> Iterable[str]:
    pg_storage = get_postgres_storage(request_dict)
    query, params = parse_query(request_dict.get('sql_query'))
    return (row[0] for row in pg_storage.exec_query(query, params))


def get_text_corpus_from_file(file) -> Iterable[str]:
    filename = pathlib.Path(file.filename).name
    if filename.endswith('.pdf'):
        pdf = pdftotext.PDF(file)
        return (page.replace('\n', ' ') for page in pdf)
    filepath = os.path.join(app.instance_path, Config.TMP_DATA_FOLDER, filename)
    file.save(filepath)
    content = textract.process(filepath)
    os.remove(filepath)
    return (text.replace('\n', ' ') for text in content.decode().split('\n\n'))


def get_text_corpus_gen_from_folder(request):
    for filename in request.files:
        try:
            yield True, filename, get_text_corpus_from_file(request.files[filename])
        except ExtensionNotSupported:
            yield False, filename, None
