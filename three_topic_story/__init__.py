from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, IMAGES, configure_uploads
from .config import config_dict
import click

db = SQLAlchemy()
bootstrap = Bootstrap5()
bcrypt = Bcrypt()
migrate = Migrate(compare_type=True)
mail = Mail()
login = LoginManager()
jwt = JWTManager()
uploads_images = UploadSet(name='images', extensions=IMAGES)

tags = []
with open('three_topic_story/static/wordlist.txt', 'r') as f:
    for word in f:
        tags.append(word[:-1])

from .commands import init_cli
from .errorhandler import init_errorhandler


def create_app(config='develop'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config])

    db.init_app(app)
    bootstrap.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    login.init_app(app)
    login.login_view = 'account.login'
    login.login_message = '請先登入您的帳號'
    jwt.init_app(app)
    configure_uploads(app, uploads_images)

    @app.context_processor
    def inject_variable():
        return dict(url=app.config['URL'])

    from three_topic_story.main import main
    app.register_blueprint(main)
    from three_topic_story.account import account
    app.register_blueprint(account, url_prefix='/account')
    from three_topic_story.post import post
    app.register_blueprint(post, url_prefix='/post')

    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db)

    init_cli(app)
    init_errorhandler(app)

    return app
