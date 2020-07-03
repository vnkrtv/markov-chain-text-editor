from flask import Flask
from config import Config
from app.context_procesor import close_icon_path, sort_icon_path, delete_icon_path, update_icon_path

app = Flask(__name__)
app.config.from_object(Config)

app.context_processor(close_icon_path)
app.context_processor(sort_icon_path)
app.context_processor(delete_icon_path)
app.context_processor(update_icon_path)
app.jinja_env.globals.update(close_icon=close_icon_path)
app.jinja_env.globals.update(sort_icon=sort_icon_path)
app.jinja_env.globals.update(delete_icon=delete_icon_path)
app.jinja_env.globals.update(update_icon=update_icon_path)


from app import routes
