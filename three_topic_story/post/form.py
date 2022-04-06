from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, TextAreaField, BooleanField, HiddenField
from .model import Post
from flask_login import current_user


class FormEditPost(FlaskForm):
    title = StringField('標題', validators=[
        validators.DataRequired(),
        validators.Length(1, 80)
    ])
    body = TextAreaField('內容', validators=[
        validators.DataRequired()
    ])

    tags = HiddenField('tags')
    private = BooleanField('不公開')

    submit = SubmitField('完成')
