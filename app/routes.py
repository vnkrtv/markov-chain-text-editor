from app import app
from app import forms
from flask import render_template
from flask.views import MethodView
from googletrans import Translator
from models.markov.markov_model import MarkovModel
from models.utils.postgres import PostgresStorage
# from models.gpt2.generate_samples import interact_model

storage = PostgresStorage.connect(host='172.17.0.2')
texts_list = storage.get_posts_texts()
print('Loaded texts: ', len(texts_list))
markov_model = MarkovModel(order=5)
markov_model.train(texts_list)
print('Marcov model len: ', len(markov_model.model))
markov_model.save()


class ArticlesGenAPI(MethodView):
    template = 'index.html'
    context = {
        'title': 'Генератор определений',
    }
    translator = Translator()
    # storage = PostgresStorage.connect(host='172.17.0.2')
    # texts_list = storage.get_posts_texts()

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
            self.context['text_samples'] = [
                markov_model.generate_by_phrase(30, phrase)
                for _ in range(form.samples_count.data)
            ]
        return render_template(self.template, **self.context)


app.add_url_rule('/',
                 view_func=ArticlesGenAPI.as_view('api'),
                 methods=['POST', 'GET'])
