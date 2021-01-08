import re
from datetime import datetime, timedelta

from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from app import app, db, csrf, markov
from .models import (
    User, Document, MarkovModel)
from .markov import (
    get_text_corpus_from_file, get_text_corpus_from_postgres)
from .forms import (
    LoginForm, RegistrationForm, DocumentForm, ModelForm)


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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/document/<int:document_id>', methods=['GET', 'POST'])
@login_required
def document(document_id):
    form = DocumentForm()
    doc = Document.query.filter_by(id=document_id).first()
    if current_user.id == doc.user_id:
        if request.method == 'POST' and form.submit():
            doc.created = doc.created
            doc.last_update = datetime.utcnow() + timedelta(hours=3)
            doc.title = request.form.get('title', doc.title)
            doc.body = request.form.get('doc-body', doc.body)
            db.session.commit()
            flash("Document '%s' has been successfully updated." % doc.title)
            return redirect(url_for('index'))
        models = MarkovModel.query.all()
        if len(models):
            model = models[0]
            model.load()
            return render_template('editor.html', title=doc.title, doc=doc, form=form)
        else:
            flash("No available models found. Add new model to start working with documents.")
    return redirect(url_for('index'))


class IndexView(MethodView):
    template = 'documents.html'
    decorators = [login_required]

    def get(self):
        context = {
            'title': 'Documents',
            'documents': Document.query.filter_by(user_id=current_user.id).all(),
            'doc_form': DocumentForm(),
            'model_form': ModelForm()
        }
        return render_template(self.template, **context)

    def post(self):
        doc_form = DocumentForm()
        model_form = ModelForm()
        if doc_form.validate_on_submit():
            doc = Document(title=doc_form.title.data, user_id=current_user.id)
            db.session.add(doc)
            db.session.commit()
            return redirect(url_for('document', document_id=doc.id))
        elif doc_form.is_submitted():
            flash(''.join(doc_form.title.errors))

        if model_form.validate_on_submit():
            try:
                data_source = request.form.get('data_source')
                if data_source == 'file':
                    train_corpus = get_text_corpus_from_file(request)
                elif data_source == 'postgres':
                    train_corpus = get_text_corpus_from_postgres(request.form)
                else:
                    flash('Data source must be specified for added model.')
                    return self.get()

                model = MarkovModel.train(train_corpus=train_corpus,
                                          model_name=model_form.name.data,
                                          state_size=model_form.state_size.data,
                                          use_ngrams=model_form.use_ngrams.data,
                                          ngram_size=model_form.ngram_size.data)
                model.load()
                db.session.add(model)
                db.session.commit()
                flash("New model '%s' was successfully added." % model.name)
            except Exception as e:
                flash("Error: %s" % str(e))
        elif model_form.is_submitted():
            flash(''.join(model_form.name.errors))

        return self.get()


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
        return render_template(self.template, title=self.title, form=form)


class GeneratorView(MethodView):
    title = 'Phrases generator'
    template = 'generate.html'

    def get(self):
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        models = MarkovModel.query.all()
        return render_template(self.template, title=self.title, models=models)

    def post(self):
        return self.get()


class GeneratorAPI(MethodView):
    decorators = [csrf.exempt]
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    def get(self):
        return redirect(url_for('index'))

    def post(self):
        model_id = int(request.form['modelID'])
        phrase = request.form['phrase']
        samples_num = int(request.form['samplesNum'])

        model = MarkovModel.query.get(model_id)
        model.load()
        processed_phrase = self.remove_punctuation.sub('', phrase).strip()

        return jsonify({
            'samples': model.generate_samples(processed_phrase, samples_num)
        })


class T9API(MethodView):
    decorators = [csrf.exempt]
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    def get(self):
        return redirect(url_for('index'))

    def post(self):
        model = markov.get_model()
        beginning = self.remove_punctuation.sub('', request.form['beginning']).strip()

        first_words_count = int(request.form['first_words_count'])
        phrase_len = int(request.form['phrase_length'])
        return jsonify({
            'words': model.make_sentences_for_t9(
                beginning, first_words_count, phrase_len)
        })


class ModelsAPI(MethodView):
    decorators = [csrf.exempt]

    def get(self):
        models = MarkovModel.query.all()
        return jsonify({
            'models': [model.name for model in models]
        })

    def post(self):
        model = MarkovModel.query.filter_by(name=request.form['model_name']).first()
        model.load()
        return jsonify({
            'success': "ok"
        })


app.add_url_rule('/documents',
                 view_func=IndexView.as_view('index'),
                 methods=['POST', 'GET'])
app.add_url_rule('/',
                 view_func=LoginView.as_view('login'),
                 methods=['POST', 'GET'])
app.add_url_rule('/generator',
                 view_func=GeneratorView.as_view('generator'),
                 methods=['POST', 'GET'])
app.add_url_rule('/t9',
                 view_func=T9API.as_view('t9'),
                 methods=['POST', 'GET'])
app.add_url_rule('/gen_api',
                 view_func=GeneratorAPI.as_view('gen_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/api/models',
                 view_func=ModelsAPI.as_view('models_api'),
                 methods=['POST', 'GET'])
