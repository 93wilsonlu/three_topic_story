from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_mail import Mail
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from .config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
mail = Mail(app)
login = LoginManager(app)
jwt = JWTManager(app)

# import all app
from three_topic_story.main import main
app.register_blueprint(main)
from three_topic_story.account import account
app.register_blueprint(account, url_prefix='/account')

from . import commands