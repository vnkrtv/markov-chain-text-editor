from app import app
from flask import render_template, jsonify, request, redirect, url_for
from flask.views import MethodView
from .model import get_model

MODEL_NAME = '10k.json'


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='DOC Editor')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html', title='DOC Editor')


class T9API(MethodView):

    def get(self):
        return redirect(url_for('index'))

    def post(self):
        markov_model = get_model()
        beginning = request.form['beginning']
        first_words_count = int(request.form['first_words_count'])
        phrase_len = int(request.form['phrase_length'])
        return jsonify({
            'words': markov_model.get_phrases_for_t9(beginning, first_words_count, phrase_len)
        })


app.add_url_rule('/t9',
                 view_func=T9API.as_view('t9'),
                 methods=['POST', 'GET'])
