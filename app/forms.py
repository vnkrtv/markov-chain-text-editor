from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, BooleanField, IntegerField)
from wtforms.validators import (
    ValidationError, DataRequired, EqualTo, NumberRange)

from app.models import User, Document, ModelIndex


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Authorize')


class DocumentForm(FlaskForm):
    title = StringField('Document name', validators=[DataRequired()])
    submit = SubmitField('Create')

    def validate_title(self, title):
        doc = Document.query.filter_by(title=title.data).first()
        if doc is not None:
            raise ValidationError('Please use a different document title.')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class ModelForm(FlaskForm):
    name = StringField('Model name', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_name(self, name):
        model = ModelIndex.query.filter_by(name=name.data).first()
        if model is not None:
            raise ValidationError('Please use a different model name.')
