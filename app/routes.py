import re
import logging
from datetime import datetime, timedelta
from typing import Optional

from flask import render_template, jsonify, request, redirect, url_for, flash
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user
from textract.exceptions import ExtensionNotSupported

from engine.markov.utils import TextProcessor
from app import app, db, csrf, utils
from .models import (
    User, Document, ModelIndex)
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
        models = ModelIndex.query.all()
        if len(models):
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
            'doc_form': DocumentForm()
        }
        return render_template(self.template, **context)

    def post(self):
        doc_form = DocumentForm()
        if doc_form.validate_on_submit():
            doc = Document(title=doc_form.title.data, user_id=current_user.id)
            db.session.add(doc)
            db.session.commit()
            return redirect(url_for('document', document_id=doc.id))
        elif doc_form.is_submitted():
            flash(''.join(doc_form.title.errors))
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


class T9API(MethodView):
    decorators = [csrf.exempt]
    remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')

    def post(self):
        phrase = self.remove_punctuation.sub('', request.form['beginning'])
        es = utils.get_elastic_engine()
        sentences = es.get(index_name=request.form['indexName'], phrase=phrase)
        print('phrase: ', phrase, '\nsentences: ', sentences)
        return jsonify({
            'sentences': sentences
        })


class ModelsView(MethodView):
    title = 'Models'
    template = 'models.html'

    def get(self):
        context = {
            'title': self.title,
            'models': ModelIndex.query.all(),
            'models_stats': ModelIndex.get_indices_stats(),
            'model_form': ModelForm()
        }
        return render_template(self.template, **context)

    def post(self):
        model_form = ModelForm()
        if model_form.validate_on_submit():
            try:
                data_source = request.form.get('data_source')
                if data_source == 'file':
                    train_corpus = utils.get_text_corpus_from_file(request, filename='train_file')
                elif data_source == 'postgres':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                elif data_source == 'folder':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                else:
                    flash('Data source must be specified for added model.')
                    return self.get()

                model = ModelIndex(name=model_form.name.data)
                db.session.add(model)
                db.session.commit()

                model.create_index()
                model.update_index(
                    train_sentences=(' '.join(words) for words in TextProcessor.get_words_gen(train_corpus)))
                flash("New model '%s' was successfully added." % model.name)
            except ExtensionNotSupported as e:
                flash("Error: %s" % str(e))
            except Exception as e:
                db.session.delete(model)
                db.session.commit()
                flash("Error: %s" % str(e))
        elif model_form.is_submitted():
            flash(''.join(model_form.name.errors))
        return self.get()


class ModelsAPI(MethodView):
    decorators = [csrf.exempt]

    def get(self, model_id: str):
        try:
            if model_id == 'all':
                indices_stats = ModelIndex.get_indices_stats()
                return jsonify([
                    {
                        'id': model.id,
                        'name': model.name,
                        'index_name': model.index_name,
                        'doc_count': indices_stats[model.index_name]['doc_count'],
                        'size': indices_stats[model.index_name]['size']
                    } for model in ModelIndex.query.all()
                ])
            model = ModelIndex.query.filter_by(id=int(model_id)).first()
            index_stats = ModelIndex.get_indices_stats(index_name=model.index_name)
            return jsonify({
                'id': model.id,
                'name': model.name,
                'index_name': model.index_name,
                'doc_count': index_stats[model.index_name]['doc_count'],
                'size': index_stats[model.index_name]['size']
            })
        except Exception as e:
            return jsonify({
                'error': 'Error on getting models: %s' % e
            })

    def delete(self, model_id: str):
        model = ModelIndex.query.filter_by(id=int(model_id)).first()
        if model:
            msg = "Model '%s' was successfully deleted." % model.name
            model.delete_index()
            db.session.delete(model)
            db.session.commit()
            return jsonify({
                'success': msg
            })
        return jsonify({
            'error': "Not found"
        })

    def put(self, model_id: str):
        model = ModelIndex.query.filter_by(id=int(model_id)).first()
        if model:
            model.name = request.form['name']
            db.session.commit()
            try:
                data_source = request.form.get('data_source')
                if data_source == 'file':
                    train_corpus = utils.get_text_corpus_from_file(request, filename='train_file')
                elif data_source == 'postgres':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                elif data_source == 'folder':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                else:
                    return jsonify({
                        'error': 'Data source must be specified for added model.'
                    })
                model.update_index(
                    train_sentences=(' '.join(words) for words in TextProcessor.get_words_gen(train_corpus)))
                return jsonify({
                    'success': f"Model '%s' was successfully updated" % model.name
                })
            except ExtensionNotSupported as e:
                return jsonify({
                    'error': "Error: %s" % str(e)
                })
            except Exception as e:
                return jsonify({
                    'error': "Error: %s" % str(e)
                })
        return jsonify({
            'error': "Not found"
        })

    def post(self, model_id: str):
        if model_id == 'new':
            model = ModelIndex(name=request.form['name'])
            db.session.add(model)
            db.session.commit()
            try:
                data_source = request.form.get('data_source')
                if data_source == 'file':
                    train_corpus = utils.get_text_corpus_from_file(request, filename='train_file')
                elif data_source == 'postgres':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                elif data_source == 'folder':
                    train_corpus = utils.get_text_corpus_from_postgres(request.form)
                else:
                    return jsonify({
                        'error': 'Data source must be specified for added model.'
                    })
                model.create_index()
                model.update_index(
                    train_sentences=(' '.join(words) for words in TextProcessor.get_words_gen(train_corpus)))
                return jsonify({
                    'success': "New model '%s' was successfully added." % model.name
                })
            except ExtensionNotSupported as e:
                return jsonify({
                    'error': "Error: %s" % str(e)
                })
            except Exception as e:
                db.session.delete(model)
                db.session.commit()
                return jsonify({
                    'error': "Error: %s" % str(e)
                })


# class GeneratorView(MethodView):
#     title = 'Phrases generator'
#     template = 'generate.html'
#
#     def get(self):
#         if not current_user.is_authenticated:
#             return redirect(url_for('index'))
#         models = ModelIndex.query.all()
#         return render_template(self.template, title=self.title, models=models)
#
#     def post(self):
#         return self.get()
#
#
# class GeneratorAPI(MethodView):
#     decorators = [csrf.exempt]
#     remove_punctuation = re.compile(r'[^a-zA-Zа-яА-Я ]')
#
#     def get(self):
#         return redirect(url_for('index'))
#
#     def post(self):
#         model_id = int(request.form['modelID'])
#         phrase = request.form['phrase']
#         samples_num = int(request.form['samplesNum'])
#
#         model = ModelIndex.query.get(model_id)
#         model.load()
#         processed_phrase = self.remove_punctuation.sub('', phrase).strip()
#
#         return jsonify({
#             'samples': model.generate_samples(processed_phrase, samples_num)
#         })


app.add_url_rule('/documents',
                 view_func=IndexView.as_view('index'),
                 methods=['POST', 'GET'])
app.add_url_rule('/',
                 view_func=LoginView.as_view('login'),
                 methods=['POST', 'GET'])
app.add_url_rule('/models',
                 view_func=ModelsView.as_view('models'),
                 methods=['POST', 'GET'])
app.add_url_rule('/api/t9',
                 view_func=T9API.as_view('t9_api'),
                 methods=['POST', 'GET'])
app.add_url_rule('/api/models/<model_id>',
                 view_func=ModelsAPI.as_view('models_api'),
                 methods=['POST', 'GET', 'PUT', 'DELETE'])
# app.add_url_rule('/generator',
#                  view_func=GeneratorView.as_view('generator'),
#                  methods=['POST', 'GET'])
# app.add_url_rule('/gen_api',
#                  view_func=GeneratorAPI.as_view('gen_api'),
#                  methods=['POST', 'GET'])
