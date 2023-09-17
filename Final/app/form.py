from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirmation = PasswordField('Confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Sign in')


class QuoteForm(FlaskForm):
    title = StringField('book')
    author = StringField('author')
    content = TextAreaField('quote', validators=[DataRequired()])
    submit = SubmitField('Add to Quotes')

class WordForm(FlaskForm):
    word = StringField('word', validators=[DataRequired()])
    part_of_speech = StringField('part of speech')
    synonym = StringField('synonym')
    definition = TextAreaField('definition')
    example = TextAreaField('definition')
    submit = SubmitField('Add to Words')

class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken')

class ResetForm(FlaskForm): 
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')
    
    def check_email(self, email):
        user = User.guery.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Please register first')
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirmation = PasswordField('Confirmation', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')
