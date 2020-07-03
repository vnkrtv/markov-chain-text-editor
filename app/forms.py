from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class PhraseForm(FlaskForm):
    phrase = StringField('Фраза', validators=[DataRequired()])
    samples_count = IntegerField('Количество образцов', validators=[NumberRange(min=1, max=10), DataRequired()])
    submit = SubmitField('Сгенерировать')
