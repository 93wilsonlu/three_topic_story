from flask_wtf import FlaskForm
from wtforms import validators, EmailField, PasswordField, StringField, SubmitField, BooleanField, TextAreaField, ValidationError
from flask_wtf.file import FileAllowed, FileField
from .model import User
from three_topic_story import uploads_images
from flask_login import current_user


class FormRegister(FlaskForm):
    username = StringField('用戶名', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])
    email = EmailField('信箱', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(1, 50)
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(8, 20),
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
        validators.Email(),
        validators.Length(1, 50)
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])
    remember_me = BooleanField('記得我', default=True)
    submit = SubmitField('登入')


class FormSetting(FlaskForm):
    email = EmailField('信箱', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(1, 50)
    ])
    username = StringField('用戶名', validators=[
        validators.DataRequired(),
        validators.Length(1, 30)
    ])
    about_me = TextAreaField('我的簡介')
    avatar = FileField('頭像', validators=[
        FileAllowed(uploads_images, '這不是圖片')
    ])
    submit = SubmitField('更新')

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user and user != current_user:
            raise ValidationError('信箱已被使用')

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user and user != current_user:
            raise ValidationError('用戶名已被使用')


class FormChangePassword(FlaskForm):
    old_password = PasswordField('舊密碼', validators=[
        validators.DataRequired(),
    ])
    password = PasswordField('新密碼', validators=[
        validators.DataRequired(),
        validators.Length(8, 20),
        validators.EqualTo('password2', message='密碼不相同')
    ])
    password2 = PasswordField('確認密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('送出')


class FormForgotPassword(FlaskForm):
    email = EmailField('信箱', validators=[
        validators.DataRequired(),
        validators.Email(),
        validators.Length(1, 50)
    ])
    submit = SubmitField('送出')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('帳號不存在')


class FormResetPassword(FlaskForm):
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(8, 20),
        validators.EqualTo('password2', message='密碼不相同')
    ])
    password2 = PasswordField('確認密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('重設密碼')
