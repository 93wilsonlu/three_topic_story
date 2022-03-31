from flask_wtf import FlaskForm
from wtforms import validators, EmailField, PasswordField, StringField, SubmitField, BooleanField, ValidationError
from .model import User


class FormRegister(FlaskForm):
    username = StringField(
        '用戶名', validators=[validators.DataRequired()])
    email = EmailField('信箱', validators=[validators.DataRequired(
    ), validators.Email()])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password2', message='密碼不相同')
    ])
    password2 = PasswordField('確認密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('Register New Account')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register by somebody')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('UserName already register by somebody')


class FormLogin(FlaskForm):
    email = EmailField('信箱', validators=[
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])
    remember_me = BooleanField('記得我')
    submit = SubmitField('Log in')
