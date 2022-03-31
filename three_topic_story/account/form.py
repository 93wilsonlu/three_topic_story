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
    submit = SubmitField('註冊')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用戶名已被使用')


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


class FormSetting(FlaskForm):
    username = StringField(
        '用戶名', validators=[validators.DataRequired()])
    email = EmailField('信箱', validators=[validators.DataRequired(
    ), validators.Email()])
    about_me = StringField('我的簡介')
    submit = SubmitField('更新')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被使用')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用戶名已被使用')
