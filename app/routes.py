from app import app, db
from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user
from .models import User
from .model import get_model
from .forms import LoginForm, RegistrationForm

MODEL_NAME = '10k.json'


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', title='DOC Editor')


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


class LoginView(MethodView):
    title = 'Login'
    template = 'login.html'

    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template(self.template, title=self.title, form=LoginForm())

    def post(self):
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
        return render_template('login.html', title=self.title, form=form)


class T9API(MethodView):

    def get(self):
        return redirect(url_for('index'))

    def post(self):
        markov_model = get_model(MODEL_NAME)
        beginning = request.form['beginning']
        first_words_count = int(request.form['first_words_count'])
        phrase_len = int(request.form['phrase_length'])
        return jsonify({
            'words': markov_model.get_phrases_for_t9(beginning, first_words_count, phrase_len)
        })


app.add_url_rule('/login',
                 view_func=LoginView.as_view('login'),
                 methods=['POST', 'GET'])
app.add_url_rule('/t9',
                 view_func=T9API.as_view('t9'),
                 methods=['POST', 'GET'])
