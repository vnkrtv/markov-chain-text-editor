from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.context_procesor import user_icon_path, add_doc_icon_path, add_icon_path, gears_icon_path

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.context_processor(user_icon_path)
app.context_processor(add_doc_icon_path)
app.context_processor(add_icon_path)
app.context_processor(gears_icon_path)
app.jinja_env.globals.update(user_icon=user_icon_path)
app.jinja_env.globals.update(add_doc_icon=add_doc_icon_path)
app.jinja_env.globals.update(add_icon=add_icon_path)
app.jinja_env.globals.update(gears_icon=gears_icon_path)


from app import routes

# TODO: 1. Реализовать итеративную загрузку данных (обучение модели)
# TODO: 2. Параметрически задавать количество первых слов (в продолжении)
# TODO: 3. Собственная реализация с кодированием слов (токенов)
# TODO: 3.0 Произвести анализ использования ресурсов на каждом этапе обучения модели


# TODO: 1. Загрузить хабр и вики в индексы
# TODO: 2. Виртуалка с эластиком и приложением
# TODO: 3. Виджет для браузера
# TODO: 4. Пробел - слово, 1 слово
# TODO: 5. Курсор по середине

# Автоматизация подготовки текстовых материалов специальной предметной области
# Программное средство отслеживания упоминаемости в СМИ
