import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS

from config import Config
from app.context_procesor import (
    user_icon_path, add_doc_icon_path, add_icon_path, gears_icon_path, line_icon_path,
    update_icon_path, delete_icon_path, sort_icon_path, doc_icon_path, logout_icon_path)

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/api/*": {"origins": "*"}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)

csrf = CSRFProtect(app)
csrf.init_app(app)

login = LoginManager(app)
login.login_view = 'login'

os.makedirs(os.path.join(app.instance_path, Config.TMP_DATA_FOLDER), exist_ok=True)

app.context_processor(user_icon_path)
app.context_processor(add_doc_icon_path)
app.context_processor(add_icon_path)
app.context_processor(gears_icon_path)
app.context_processor(update_icon_path)
app.context_processor(delete_icon_path)
app.context_processor(sort_icon_path)
app.context_processor(doc_icon_path)
app.context_processor(logout_icon_path)
app.context_processor(line_icon_path)
app.jinja_env.globals.update(user_icon=user_icon_path)
app.jinja_env.globals.update(add_doc_icon=add_doc_icon_path)
app.jinja_env.globals.update(add_icon=add_icon_path)
app.jinja_env.globals.update(gears_icon=gears_icon_path)
app.jinja_env.globals.update(update_icon=update_icon_path)
app.jinja_env.globals.update(delete_icon=delete_icon_path)
app.jinja_env.globals.update(sort_icon=sort_icon_path)
app.jinja_env.globals.update(doc_icon=doc_icon_path)
app.jinja_env.globals.update(logout_icon=logout_icon_path)
app.jinja_env.globals.update(line_icon=line_icon_path)


from app import routes

# DONE: 1. Реализовать итеративную загрузку данных (обучение модели)
# DONE: 2. Параметрически задавать количество первых слов (в продолжении)
# DONE: 3. Собственная реализация с кодированием слов (токенов)
# DONE: 3.0 Произвести анализ использования ресурсов на каждом этапе обучения модели

# TODO: Выгрузка с папки

# TODO: 1. Загрузить хабр и вики в индексы
# TODO: 2. Виртуалка с эластиком и приложением -
# TODO: 3. Виджет для браузера
# DONE: 4. Пробел - слово, 1 слово
# DONE: 5. Курсор по середине

# Автоматизация подготовки текстовых материалов специальной предметной области
# Программное средство отслеживания упоминаемости в СМИ
