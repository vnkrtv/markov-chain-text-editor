from app import app
from app import forms
from flask import render_template, jsonify
from flask.views import MethodView
from googletrans import Translator
from .model import get_model
# from models.gpt2.generate_samples import interact_model


class ArticlesGenAPI(MethodView):
    template = 'index.html'
    context = {
        'title': 'Генератор определений',
    }
    translator = Translator()

    def get(self):
        self.context['form'] = forms.PhraseForm()
        self.context['message'] = ''
        self.context['text_samples'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        form = forms.PhraseForm()
        if form.validate_on_submit():
            self.context['form'] = form
            phrase = form.phrase.data
            '''
            phrase = self.translator.translate(form.phrase.data).text
            self.context['text_samples'] = [
                form.phrase.data + ' ' + self.translator.translate(text, dest='ru').text
                for text in interact_model(
                    phrase,
                    nsamples=form.samples_count.data,
                    top_k=20,
                    temperature=0.7)
            ]
            '''
            markov_model = get_model()
            if phrase:
                text_samples = [
                    markov_model.generate_sample(phrase)
                    for _ in range(form.samples_count.data)
                ]
            else:
                text_samples = [
                    markov_model.model.make_short_sentence(500)
                    for _ in range(form.samples_count.data)
                ]
            self.context['text_samples'] = text_samples
        return render_template(self.template, **self.context)


app.add_url_rule('/',
                 view_func=ArticlesGenAPI.as_view('api'),
                 methods=['POST', 'GET'])
