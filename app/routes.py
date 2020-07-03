from app import app
from app import forms
from flask import render_template, flash
from flask.views import MethodView


class ArticlesGenAPI(MethodView):
    template = 'index.html'
    context = {
        'title': 'Генератор определений',
    }

    def update(self, form):
        if form.validate_on_submit():
            try:
                message = f'Information about purchase on total cost {form.total_cost.data} was successfully updated.'
                self.context['message'] = message
            except:
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def delete(self, form):
        self.context['message'] = f'Successfully delete purchase on total cost {form.total_cost.data} from database.'

    def add(self, form):
        if form.validate_on_submit():
            try:
                message = f'Purchase on total cost {form.total_cost.data} was successfully added to database.'
                self.context['message'] = message
            except:
                flash('Error on inserting value into table.')
        else:
            flash('Invalid form data.')

    def get(self):
        self.context['form'] = forms.PhraseForm()
        self.context['message'] = ''
        return render_template(self.template, **self.context)

    def post(self):
        self.context['form'] = forms.PhraseForm()
        return render_template(self.template, **self.context)


app.add_url_rule('/',
                 view_func=ArticlesGenAPI.as_view('api'),
                 methods=['POST', 'GET'])
