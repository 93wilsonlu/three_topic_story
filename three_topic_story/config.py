import os
import datetime


class Config:
    project_dir = os.path.abspath(os.path.dirname(__file__))

    DEBUG = True

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(project_dir, 'static/data/data.sqlite')

    SECRET_KEY = os.environ['SECRET_KEY']

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PROT = 465
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']

    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)

    SESSION_PROTECTION = 'strong'

    UPLOADED_IMAGES_DEST = os.path.join(project_dir, 'static/img')
    UPLOADED_IMAGES_URL = '/static/img/'
