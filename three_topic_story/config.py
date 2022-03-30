import os
import datetime

project_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
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


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(project_dir, 'static/data/data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


config_dict = {'develop': DevelopmentConfig,
               'product': ProductionConfig}
