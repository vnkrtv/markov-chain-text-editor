from app import app
from app import forms
from flask import render_template, flash
from flask.views import MethodView


class ArticlesGenAPI(MethodView):
    template = 'index.html'
    context = {
        'title': 'Генератор определений',
    }

    def get(self):
        self.context['form'] = forms.PhraseForm()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        form = forms.PhraseForm()
        if form.validate_on_submit():
            self.context['message'] = form.phrase.data
        else:
            self.context['message'] = 'blya'
        self.context['form'] = form
        return render_template(self.template, **self.context)


app.add_url_rule('/',
                 view_func=ArticlesGenAPI.as_view('api'),
                 methods=['POST', 'GET'])
