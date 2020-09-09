from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from app.context_procesor import save_icon_path, sort_icon_path, delete_icon_path, update_icon_path

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

app.context_processor(save_icon_path)
app.context_processor(sort_icon_path)
app.context_processor(delete_icon_path)
app.context_processor(update_icon_path)
app.jinja_env.globals.update(save_icon=save_icon_path)
app.jinja_env.globals.update(sort_icon=sort_icon_path)
app.jinja_env.globals.update(delete_icon=delete_icon_path)
app.jinja_env.globals.update(update_icon=update_icon_path)


from app import routes

# TODO: 1. Реализовать итеративную загрузку данных (обучение модели)
# TODO: 2. Параметрически задавать количество первых слов (в продолжении)
# TODO: 3. Собственная реализация с кодированием слов (токенов)
# TODO: 3.0 Произвести анализ использования ресурсов на каждом этапе обучения модели
